<script lang="ts">
    import { onMount } from "svelte";
    import { fade, scale } from "svelte/transition";

    import { socket, initializeSocket } from "./lib/socket.js";
    import { get } from "svelte/store";

    import { iterateLayers, drawArrow, drawText} from "./lib/drawing.js";
    import type { Socket, SocketOptions } from "socket.io-client";
    import FpsLed from "./lib/FpsLed.svelte";
    import Led from "./lib/Led.svelte";
    import TelemetryScreen from "./lib/TelemetryScreen.svelte";
    import { getFormationData, getFormationsCount } from "./lib/Formations.js";
    import { getRobotControlDataControlDecoder, getRobotControlDataTransnet } from "./lib/RobotControl.js";

    let fpsLed: FpsLed;

    let innerWidth = $state(window.innerWidth);
    let innerHeight = $state(window.innerHeight);

    let showTop = $state(false);
    let showRight = $state(true);
    let showBottom = $state(true);
    let showLeft = $state(false);

    let maximizeBottom = $state(false);

    let topHeight = $state(150);
    let rightWidth = $state(200);
    let bottomHeight = $derived(maximizeBottom ? innerHeight * 0.8 : 200);
    let leftWidth = $state(150);

    let offsetLeft = $derived(showLeft ? leftWidth : 0);
    let offsetTop = $derived(showTop ? topHeight : 0);
    let offsetWidth = $derived(
        innerWidth - (showLeft ? leftWidth : 0) - (showRight ? rightWidth : 0),
    );
    let offsetHeight = $derived(
        innerHeight -
            (showTop ? topHeight : 0) -
            (showBottom ? bottomHeight : 0),
    );

    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;

    $effect(() => {
        canvas.width = innerWidth;
        canvas.height = innerHeight;
    });

    let divFields: Record<string, HTMLImageElement> = {
        divB: new Image(),
        divC: new Image(),
    };
    Object.keys(divFields).forEach((division) => {
        const field = new Image();
        field.onload = function () {
            console.log("Field " + division, field.width, field.height);
            divFields[division] = field;
        };
        field.src = `/static/images/field_${division}.svg`;
    });

    const ALLOWED_DIVISIONS = ["divB", "divC"] as const;
    type Division = (typeof ALLOWED_DIVISIONS)[number];

    let currentDivision: Division = "divB";
    let zoomParams = {
        divB: 0.13,
        divC: 0.25,
    };
    let currentVersion = $state("undefined");

    let layer_data = $state({});
    let telemetry_data = $state({});
    let telemetry_to_display = $state(["", "", ""]);
    let telemetry_width = $derived(
        100 / telemetry_to_display.filter((t) => t !== "").length,
    );

    // $inspect(layer_data)

    class Connection {
        currentTime = $state(0);
        lastUpdateTime = $state(0);
        connectionTimeout = 1000;
        isOnline = $derived(
            this.currentTime - this.lastUpdateTime < this.connectionTimeout,
        );
        color = $derived(this.isOnline ? "#00ff00" : "#ff0000");

        constructor() {
            this.lastUpdateTime = 0;
        }

        update() {
            this.currentTime = Date.now();
        }

        ping() {
            this.lastUpdateTime = Date.now();
        }
    }

    let servizConnection = new Connection();
    let transnetConnection = new Connection();

    // $inspect("serviz", servizConnection.currentTime, servizConnection.lastUpdateTime);
    // $inspect(servizConnection.isOnline);

    // $inspect("transnet", transnetConnection.currentTime, transnetConnection.lastUpdateTime);
    // $inspect(transnetConnection.isOnline);

    class Camera {
        panX = $state(0);
        panY = $state(0);
        zoom = $state(1);
        zoomParam = $state(1);
        canvasWidth = $state(0);
        canvasHeight = $state(0);

        offsetX = $derived(this.panX + this.canvasWidth / 2);
        offsetY = $derived(this.panY + this.canvasHeight / 2);

        constructor(
            panX: number,
            panY: number,
            zoom: number,
            zoomParam: number,
        ) {
            this.panX = panX;
            this.panY = panY;
            this.zoom = zoom;
            this.zoomParam = zoomParam;
        }

        reset() {
            this.panX = 0;
            this.panY = 0;
            this.zoom = 1;
            resizeCanvas();
        }

        pan(x: number, y: number) {
            this.panX += x;
            this.panY += y;
        }

        changeZoom(
            factor: number,
            clientX = this.canvasWidth / 2,
            clientY = this.canvasHeight / 2,
        ) {
            // console.log(this.panX.toFixed(2), this.panY.toFixed(2), clientX, clientY);
            // console.log("field2scr", camera.field_mm2screen(1000, 0));
            // console.log("scr2field", camera.screen2field_mm(clientX, clientY));
            // const old_zoom = this.zoom * this.zoomParam;

            this.zoom *= factor;
            this.zoom = Math.min(Math.max(camera.zoom, 0.5), 3);
            // const new_zoom = this.zoom * this.zoomParam;

            // const [fieldX, fieldY] = this.screen2field_mm(clientX, clientY);
            // // this.panX = this.panX - (clientX / old_zoom) + (clientY / new_zoom);
            // this.panX = this.offsetX - this.canvasWidth / 2 + (clientX) * (new_zoom - old_zoom);
            // this.panX = this.panX - (clientX / old_zoom) + (clientX / new_zoom);
            // this.panY = this.panY - (clientY / old_zoom) + (clientY / new_zoom);
        }

        screen2field_mm(scr_x: number, scr_y: number) {
            const field_x =
                (scr_x + (-this.canvasWidth / 2 - this.panX)) /
                (this.zoom * this.zoomParam);
            const field_y =
                (scr_y + (-this.canvasHeight / 2 - this.panY)) /
                (this.zoom * this.zoomParam);
            return [field_x, field_y];
        }

        field_mm2screen(field_x: number, field_y: number) {
            const scr_x =
                field_x * (this.zoom * this.zoomParam) +
                (-this.canvasWidth / 2 - this.panX);
            const scr_y =
                field_y * (this.zoom * this.zoomParam) +
                (-this.canvasHeight / 2 - this.panY);
            return [scr_x, scr_y];
        }

        transcale(ctx: CanvasRenderingContext2D) {
            ctx.translate(this.offsetX, this.offsetY);
            ctx.scale(this.zoom * this.zoomParam, this.zoom * this.zoomParam);
        }
    }

    let camera = $state(new Camera(0, 0, 1, zoomParams[currentDivision]));

    $effect(() => {
        camera.canvasWidth = offsetWidth;
        camera.canvasHeight = offsetHeight;
    });

    $effect(() => {
        console.log("View update: ", camera);
    });

    let isDragging = false;
    let startX = 0;
    let startY = 0;

    let isBallDragging = false;
    let startBallX = 0;
    let startBallY = 0;
    let deltaBallX = 0;
    let deltaBallY = 0;
    const velScaleFactor = 4;

    let isCursorPosShowEnabled = $state(false);
    let cursorPos = [0, 0];

    let fieldOrientation = $state(false);
    let useNumberIds = $state(false);
    let isRobotControlEnabled = $state(false);

    let panAmount = 100;

    let showHelp = $state(false);

    const hotkeys = [
        // Show help
        {
            keys: ["?"],
            description: "Show help",
            callback: (e: KeyboardEvent) => (showHelp = !showHelp),
        },
        // Movement
        {
            keys: ["r"],
            description: "Reset camera position",
            callback: (e: KeyboardEvent) => camera.reset(),
        },
        {
            keys: ["ArrowUp", "k"],
            description: "Pan up",
            callback: (e: KeyboardEvent) => camera.pan(0, panAmount),
        },
        {
            keys: ["ArrowDown", "j"],
            description: "Pan down",
            callback: (e: KeyboardEvent) => camera.pan(0, -panAmount),
        },
        {
            keys: ["ArrowLeft", "h"],
            description: "Pan left",
            callback: (e: KeyboardEvent) => camera.pan(panAmount, 0),
        },
        {
            keys: ["ArrowRight", "l"],
            description: "Pan right",
            callback: (e: KeyboardEvent) => camera.pan(-panAmount, 0),
        },
        // Zoom
        {
            keys: ["-"],
            description: "Zoom out",
            callback: (e: KeyboardEvent) => camera.changeZoom(1 / 1.1),
        },
        {
            keys: ["="],
            description: "Zoom in",
            callback: (e: KeyboardEvent) => camera.changeZoom(1.1),
        },
        // Display parameters
        {
            keys: ["f"],
            description: "Toggle field orientation",
            callback: (e: KeyboardEvent) =>
                (fieldOrientation = !fieldOrientation),
        },
        {
            keys: ["i"],
            description: "Toggle ID display format",
            callback: (e: KeyboardEvent) => (useNumberIds = !useNumberIds),
        },
        // Control
        {
            keys: ["t"],
            description: "Test command",
            callback: testButton,
        },
        {
            keys: ["Alt + Drag"],
            description: "Launch ball",
            callback: (e: KeyboardEvent) => {},
        },
        // Layer visibility (programmatically generated)
        ...Array.from({ length: 9 }, (_, i) => ({
            keys: [`${i + 1}`],
            description: undefined,
            callback: (e: KeyboardEvent) => toggleLayerVisibilityByIndex(i + 1),
        })),
        {
            keys: ["1..9"],
            description: "Toggle visibility of layer 1..9",
            callback: (e: KeyboardEvent) => {},
        },
        {
            keys: ["m"],
            description: "Toggle manual robot control",
            callback: (e: KeyboardEvent) => {
                isRobotControlEnabled = !isRobotControlEnabled;
            },
        },
        {
            keys: ["w", "a", "s", "d", "q", "e"],
            description: "Manual robot control",
            callback: (e: KeyboardEvent) => {},
            callbackReleased: (e: KeyboardEvent) => {},
        },
    ];

    let pressed: { [key: string]: boolean } = {};

    // Key handler with support for multiple keys per command
    function handleKeydown(e: KeyboardEvent) {
        const pressedKey = e.key;

        hotkeys.some((hotkey) => {
            if (hotkey.keys.includes(pressedKey)) {
                e.preventDefault();
                hotkey.callback(e);
                pressed[e.key] = true;
                return true; // Stop checking once found
            }
        });
    }

    function handleKeyup(e: KeyboardEvent) {
        const releasedKey = e.key;

        hotkeys.some((hotkey) => {
            if (hotkey.keys.includes(releasedKey)) {
                e.preventDefault();
                if (hotkey.callbackReleased !== undefined) {
                    hotkey.callbackReleased(e);
                }
                delete pressed[e.key];
                return true; // Stop checking once found
            }
        });
    }

    function checkIfPressed(key: string): boolean {
        return pressed[key];
    }

    let vel_xy = $state(1000);
    let vel_r = $state(2);
    let robotControlTeam = $state("blue");
    let robotControlId = $state(0);

    function controlRobot() {
        let speed_x = 0;
        let speed_y = 0;
        let speed_r = 0;

        const dirs = [
            {
                key: "w",
                speed_x: vel_xy,
                speed_y: 0,
                speed_r: 0,
            },
            {
                key: "a",
                speed_x: 0,
                speed_y: -vel_xy,
                speed_r: 0,
            },
            {
                key: "s",
                speed_x: -vel_xy,
                speed_y: 0,
                speed_r: 0,
            },
            {
                key: "d",
                speed_x: 0,
                speed_y: vel_xy,
                speed_r: 0,
            },
            {
                key: "q",
                speed_x: 0,
                speed_y: 0,
                speed_r: vel_r,
            },
            {
                key: "e",
                speed_x: 0,
                speed_y: 0,
                speed_r: -vel_r,
            },
        ];

        for (const dir of dirs) {
            if (checkIfPressed(dir.key)) {
                speed_x += dir.speed_x;
                speed_y += dir.speed_y;
                speed_r += dir.speed_r;
            }
        }

        actuateRobot(robotControlTeam, robotControlId, speed_x, speed_y, speed_r);
    }

    function actuateRobot(
        team: string,
        id: number,
        speed_x: number,
        speed_y: number,
        speed_r: number,
    ) {
        let data = getRobotControlDataTransnet(
            team,
            id,
            speed_x,
            speed_y,
            speed_r
        );

        socketEmit("send_signal", data);
    }

    function testButton(e: Event) {
        console.log("test button");
        socketEmit("send_signal", {
            transnet: "test_signal",
        });
    }

    function toggleLayerVisibilityByIndex(layer_index: number) {
        layer_index -= 1;
        if (layer_index >= 0 && layer_index < Object.keys(layer_data).length) {
            const layer_name = Object.keys(layer_data)[layer_index];
            toggleLayerVisibility(layer_name);
        }
    }

    function toggleLayerVisibility(layer_name: string) {
        console.info("Toggle layer visibility", layer_name);
        socketEmit("toggle_layer_visibility", layer_name);
    }

    function clearLayers() {
        socketEmit("clear_layers", {});
        layer_data = {};
    }

    function clearTelemetry() {
        socketEmit("clear_telemetry", {});
        telemetry_data = {};
    }

    onMount(() => {
        ctx = canvas.getContext("2d", { alpha: true })!;

        window.addEventListener("resize", resizeCanvas);

        window.addEventListener("wheel", (e) => {
            if (e.deltaY > 0) {
                camera.changeZoom(1.03, e.clientX, e.clientY);
            } else {
                camera.changeZoom(1 / 1.03, e.clientX, e.clientY);
            }
        });

        canvas.addEventListener("mousedown", (e) => {
            if (e.button !== 0) return;

            isDragging = true;
            startX = e.clientX - camera.panX;
            startY = e.clientY - camera.panY;

            if (e.altKey) {
                isBallDragging = true;
            }
            [startBallX, startBallY] = camera.screen2field_mm(
                e.clientX,
                e.clientY,
            );
            deltaBallX = 0;
            deltaBallY = 0;
        });

        canvas.addEventListener("mousemove", (e) => {

            if (isCursorPosShowEnabled) {
                cursorPos = camera.screen2field_mm(e.clientX, e.clientY);
            }

            if (!isDragging) {
                return;
            }

            if (e.altKey) {
                deltaBallX = -(
                    camera.screen2field_mm(e.clientX, e.clientY)[0] - startBallX
                );
                deltaBallY = -(
                    camera.screen2field_mm(e.clientX, e.clientY)[1] - startBallY
                );
                // console.log(deltaBallX, deltaBallY);
            } else {
                camera.panX = e.clientX - startX;
                camera.panY = e.clientY - startY;
            }
        });

        canvas.addEventListener("mouseup", (e) => {
            if (isDragging && e.altKey) {
                const x = startBallX;
                const y = startBallY;
                const vx = deltaBallX * velScaleFactor;
                const vy = deltaBallY * velScaleFactor;
                socketEmit("send_signal", {
                    transnet: "set_ball",
                    data: { x: x, y: -y, vx: vx, vy: -vy },
                });
            }
            isDragging = false;
            isBallDragging = false;
        });

        canvas.addEventListener("mouseleave", () => {
            isDragging = false;
            isBallDragging = false;
        });

        window.addEventListener("keydown", handleKeydown);
        window.addEventListener("keyup", handleKeyup);

        const socket = initializeSocket();

        socket.on("message", (message: string) => {
            // messages = [...messages, message];
        });

        socket.on("update_division", (data: string) => {
            if (!(ALLOWED_DIVISIONS as readonly string[]).includes(data)) {
                console.warn(`Invalid division: ${data}`);
                return;
            }
            currentDivision = data as Division;
            camera.zoomParam = zoomParams[currentDivision];
            console.log("Update division", data);
        });

        socket.on("update_version", (data: string) => {
            currentVersion = data;
            console.log("Update version", data);
        });

        socket.on("update_sprites", (data: any) => {
            layer_data = data;
            servizConnection.ping();
        });

        socket.on("update_telemetry", (data: any) => {
            telemetry_data = data;
        });

        resizeCanvas();
        draw(0);

        return () => {
            window.removeEventListener("resize", resizeCanvas);
            // window.removeEventListener("wheel", );
            window.removeEventListener("keydown", handleKeydown);
            socket.disconnect();
        };
    });

    function socketEmit(event: string, data: any) {
        const currentSocket = get(socket);
        if (!currentSocket) return;
        (currentSocket as Socket).emit(event, data);
    }

    function resizeCanvas() {
        innerWidth = window.innerWidth;
        innerHeight = window.innerHeight;
    }

    let lastUpdate = 0;
    let dt = $state(0);

    function draw(timestamp: number) {
        if (!ctx) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.save();
        camera.transcale(ctx);

        drawField(currentDivision, fieldOrientation ? "left" : "right");

        iterateLayers(ctx, layer_data, useNumberIds);

        if (isBallDragging) {
            const ballVel = Math.sqrt(
                Math.pow(deltaBallX, 2) + Math.pow(deltaBallY, 2),
            );
            drawArrow(ctx, startBallX, startBallY, deltaBallX, deltaBallY);
        }

        if (isCursorPosShowEnabled) {
            drawText(ctx, cursorPos[0].toFixed(0) + ", " + cursorPos[1].toFixed(0), cursorPos[0], cursorPos[1], "white", "100px", "center");
        }

        ctx.restore();

        if (isRobotControlEnabled) {
            controlRobot();
        }

        dt = timestamp - lastUpdate;
        lastUpdate = timestamp;
        fpsLed.addDt(dt);
        servizConnection.update();
        transnetConnection.update();

        requestAnimationFrame(draw);
    }

    function drawField(
        division: Division,
        field_orientation: "left" | "right",
    ) {
        ctx.save();
        if (field_orientation == "left") {
            ctx.scale(-1, 1);
        }
        ctx.drawImage(
            divFields[division],
            Math.floor(-divFields[division].width / 2),
            Math.floor(-divFields[division].height / 2),
        );
        ctx.restore();
    }
</script>

<main>
    <div class="canvas-container">
        <canvas
            bind:this={canvas}
            oncontextmenu={(e) => {
                e.preventDefault();
            }}
        ></canvas>
    </div>

    <div
        class="panel right"
        style="
        --card-background-color:#ffffffcc;
        --card-box-shadow: 0 0 10px 5px rgba(0, 0, 0, 0.1);
        top: {showTop ? topHeight : 0}px;
        bottom: {0}px;
        width: {rightWidth}px;
        right: {showRight ? 0 : -rightWidth}px;
    "
    >
        <div style="display: flex; justify-content: space-between;">
            <span>dt: {Math.round(dt)}</span>
            <span>FPS: {Math.round(1000 / dt)} </span>
            <FpsLed bind:this={fpsLed}></FpsLed>
        </div>
        <div style="display: flex; justify-content: space-between;">
            serviz
            <Led bind:color={servizConnection.color} />
            <!-- transnet
            <Led bind:color={transnetConnection.color} /> -->
        </div>
        <h3>Controls</h3>
        <div class="controls">
            <div
                style="display: grid; grid-template: auto / repeat(4, auto); grid-gap: 0.1rem; align-items: center"
            >
                <h4>Zoom:</h4>
                {camera.zoom.toFixed(2)}
                <button
                    class="button-4"
                    onclick={() => {
                        camera.changeZoom(1.1);
                    }}>+</button
                >
                <button
                    class="button-4"
                    onclick={() => {
                        camera.changeZoom(1 / 1.1);
                    }}>-</button
                >
            </div>
            <input
                class="wide"
                type="range"
                bind:value={camera.zoom}
                min="0.5"
                max="3"
                step="0.1"
            />
        </div>
        <button
            class="button-4 wide"
            onclick={() => {
                camera.reset();
            }}>Reset view</button
        >
        <button class="button-4 wide" onclick={testButton}>Test button</button>

        <button class="button-4 wide" onclick={() => {
            socketEmit("send_signal", {"telsink": "start_recording"});
        }}>Start recording</button>
        <button class="button-4 wide" onclick={() => {
            socketEmit("send_signal", {"telsink": "stop_recording"});
        }}>Stop recording</button>

        <hr />

        <h3>Display parameters</h3>
        <div>
            <input type="checkbox" bind:checked={fieldOrientation} />
            Blue left
        </div>
        <div>
            <input type="checkbox" bind:checked={useNumberIds} />
            Use number id's
        </div>
        <div>
            <input type="checkbox" bind:checked={isCursorPosShowEnabled} />
            Show cursor position
        <hr />

        <h3>Robot control</h3>
        <div>
            <input type="checkbox" bind:checked={isRobotControlEnabled} />
            Robot control
        </div>
        {#if isRobotControlEnabled}
            <div
                style="display: grid; grid-template: auto / repeat(2, auto); grid-gap: 0.1rem; align-items: center"
            >
                <select bind:value={robotControlTeam}>
                    <option value="blue">Blue</option>
                    <option value="yellow">Yellow</option>
                </select>
                <input
                    type="number"
                    style:width="50px"
                    min="0"
                    max="15"
                    bind:value={robotControlId}
                />
            </div>
            <div>
                <p>
                    Linear vel [mm/s]: {vel_xy}
                    <input
                        type="range"
                        bind:value={vel_xy}
                        min="0"
                        max="4000"
                        step="100"
                    />
                </p>
                <p>
                    Angular vel [rad/s]: {vel_r}
                    <input
                        type="range"
                        bind:value={vel_r}
                        min="0"
                        max="4"
                        step="0.1"
                    />
                </p>
            </div>
        {/if}

        <hr />
        
        <h3>Formations</h3>
        <div
                style="display: grid; grid-template: auto / repeat({getFormationsCount()}, auto); grid-gap: 0.1rem; align-items: center"
        >
        {#each {length: getFormationsCount()} as _, i}
            <button
                class="button-4"
                onclick={() => {
                    socketEmit("send_signal", getFormationData(i));
                }}
            >{i}</button>
        {/each}
        </div>
        
        <button
            class="button-4"
            onclick={() => {
                socketEmit("send_signal", getFormationData(-1));
            }}
        >Random formation</button>

        <hr />

        <h3>Layers</h3>
        {#each Object.entries(layer_data) as [name, data], i}
            <div>
                <input
                    type="checkbox"
                    bind:checked={data.is_visible}
                    onchange={() => {
                        toggleLayerVisibility(name);
                    }}
                />
                [{i + 1}]
                {name}
            </div>
        {/each}
        <div>
            <button
                class="button-4 wide"
                onclick={() => {
                    clearLayers();
                }}
            >
                Clear layers
            </button>
            <button
                class="button-4 wide"
                onclick={() => {
                    clearTelemetry();
                }}
            >
                Clear telemetry
            </button>
        </div>

        <hr />

        <div class="version-info">
            <p><kbd>?</kbd> - Show help</p>
            <p>Version: {currentVersion}</p>
        </div>
    </div>

    <div
        class="panel down"
        style="
        --card-background-color:#ffffffcc;
        --card-box-shadow: 0 0 10px 5px rgba(0, 0, 0, 0.1);
        width: {offsetWidth}px;
        left: {offsetLeft}px;
        height: {bottomHeight}px;
        bottom: {showBottom ? 0 : -bottomHeight}px;
        display: grid;
        grid-template: auto / 100px auto
    "
    >
        <!-- top: {innerHeight - (showBottom ? bottomHeight : 0)}px; -->
        <div style="display: flex; flex-direction: column;">
            <h3 style="margin: 0;">Telemetry</h3>
            <span>
                <button
                    class="button-4"
                    style="width: 45%;"
                    onclick={() => {
                        if (telemetry_to_display.length < 6) {
                            telemetry_to_display.push("");
                        }
                    }}
                >
                    +
                </button>
                <button
                    class="button-4"
                    style="width: 45%;"
                    onclick={() => {
                        if (telemetry_to_display.length > 1) {
                            telemetry_to_display.pop();
                        }
                    }}
                >
                    -
                </button>
            </span>
            {#each telemetry_to_display as _, i}
                <select bind:value={telemetry_to_display[i]}>
                    <option value="">None</option>
                    {#each Object.keys(telemetry_data) as key}
                        <option value={key}>{key}</option>
                    {/each}
                </select>
            {/each}
            <button
                class="button-4"
                onclick={() => {
                    maximizeBottom = !maximizeBottom;
                }}
            >
                {maximizeBottom ? "Restore" : "Maximize"}
            </button>
            <div style="margin-top: auto;">
                <button
                    class="button-4"
                    onclick={() => {
                        maximizeBottom = !maximizeBottom;
                    }}
                >
                    {maximizeBottom ? "Restore" : "Maximize"}
                </button>
            </div>
        </div>
        <div style="display: flex; flex-direction: row;">
            {#each telemetry_to_display as _, i}
                {#if telemetry_to_display[i] !== ""}
                    <TelemetryScreen
                        name={telemetry_to_display[i]}
                        raw_telemetry={telemetry_data[telemetry_to_display[i]]}
                        width_percent={telemetry_width}
                    />
                {/if}
            {/each}
        </div>
    </div>

    {#if showHelp}
        <div class="help-menu" transition:fade>
            <h3>Hotkeys</h3>
            {#each hotkeys as hotkey}
                {#if hotkey.description !== undefined}
                    <p>
                        <kbd>
                            {#each hotkey.keys as key, index}
                                {index > 0 ? "/" : ""}{key}
                            {/each}
                        </kbd>
                        - {hotkey.description}
                    </p>
                {/if}
            {/each}
        </div>
    {/if}
</main>

<style>
    * {
        box-sizing: border-box;
    }

    main {
        font:
            0.8rem "Liberation Mono",
            monospace;
    }

    .canvas-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 0;
    }

    .panel {
        position: fixed;
        background: var(--card-background-color);
        padding: 1rem;
        box-shadow: var(--card-box-shadow);
        z-index: 1;
        transition: all 0.3s ease;

        display: flex;
        flex-direction: column;
        /* min-height: 100vh; */ /* or fixed height if needed */

        /* top: var(--panel-top);
        height: var(--panel-height);
        bottom: var(--panel-bottom);
        left: var(--panel-left);
        width: var(--panel-width);
        right: var(--panel-right); */
    }

    hr {
        /* flex-grow: 1; */
        width: 100%; /* or this */
    }

    .help-menu {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;

        z-index: 10;
    }
    kbd {
        background-color: #eee;
        border-radius: 2px;
        border: 1px solid #b4b4b4;
        padding: 0px 2px;
        margin-right: 0px;
    }

    .version-info {
        margin-top: auto;
        text-align: right;
        padding: 0.5rem;
    }

    /* ==========================================================================
   Buttons
   ========================================================================== */

    /* <!-- HTML !-->
<button class="button-4" role="button">Button 4</button> */

    /* CSS */
    .button-4 {
        appearance: none;
        background-color: #fafbfc;
        border: 1px solid rgba(27, 31, 35, 0.15);
        border-radius: 6px;
        box-shadow:
            rgba(27, 31, 35, 0.04) 0 1px 0,
            rgba(255, 255, 255, 0.25) 0 1px 0 inset;
        box-sizing: border-box;
        color: #24292e;
        cursor: pointer;
        display: inline-block;
        /* font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"; */
        /* font-size: 14px; */
        font-weight: 500;
        line-height: 20px;
        list-style: none;
        padding: 2px 6px;
        position: relative;
        transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
        vertical-align: middle;
        white-space: nowrap;
        word-wrap: break-word;
    }

    .wide {
        width: 100%;
    }

    .button-4:hover {
        background-color: #f3f4f6;
        text-decoration: none;
        transition-duration: 0.1s;
    }

    .button-4:disabled {
        background-color: #fafbfc;
        border-color: rgba(27, 31, 35, 0.15);
        color: #959da5;
        cursor: default;
    }

    .button-4:active {
        background-color: #edeff2;
        box-shadow: rgba(225, 228, 232, 0.2) 0 1px 0 inset;
        transition: none 0s;
    }

    .button-4:focus {
        outline: 1px transparent;
    }

    .button-4:before {
        display: none;
    }

    .button-4:-webkit-details-marker {
        display: none;
    }
</style>
