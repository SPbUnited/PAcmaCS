<script lang="ts">
    let showTop = $state(false);
    let showRight = $state(true);
    let showBottom = $state(false);
    let showLeft = $state(false);

    let topHeight = $state(150);
    let rightWidth = $state(200);
    let bottomHeight = $state(150);
    let leftWidth = $state(150);

    let offsetLeft = $derived(showLeft ? leftWidth : 0);
    let offsetTop = $derived(showTop ? topHeight : 0);
    let offsetWidth = $derived(
        window.innerWidth -
            (showLeft ? leftWidth : 0) -
            (showRight ? rightWidth : 0),
    );
    let offsetHeight = $derived(
        window.innerHeight -
            (showTop ? topHeight : 0) -
            (showBottom ? bottomHeight : 0),
    );

    let canvas_window_center_x = $derived(offsetLeft + offsetWidth / 2);
    let canvas_window_center_y = $derived(offsetTop + offsetHeight / 2);

    import { onMount } from "svelte";
    import { fade } from "svelte/transition";

    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;

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

    let currentDivision: "divB" | "divC" = "divB";
    let zoomParams = {
        divB: 0.13,
        divC: 0.25,
    };
    let currentVersion = "undefined";

    class Camera {
        panX = $state(0);
        panY = $state(0);
        zoom = $state(1);
        zoomParam = $state(1);

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
        }

        pan(x: number, y: number) {
            this.panX += x;
            this.panY += y;
        }

        changeZoom(factor: number) {
            this.zoom *= factor;
            this.zoom = Math.min(Math.max(camera.zoom, 0.5), 3);
        }
    }

    let camera = $state(new Camera(0, 0, 1, zoomParams[currentDivision]));

    $effect(() => {
        console.log("View update: ", camera);
        draw();
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

    let fieldOrientation = $state(false);
    let useNumberIds = $state(false);

    let panAmount = 100;

    let showHelp = $state(false);

    const hotkeys = [
        // Show help
        {
            keys: ["?"],
            description: "Show help",
            callback: () => (showHelp = !showHelp),
        },
        // Movement
        {
            keys: ["r"],
            description: "Reset camera position",
            callback: () => camera.reset(),
        },
        {
            keys: ["ArrowUp", "k"],
            description: "Pan up",
            callback: () => camera.pan(0, panAmount),
        },
        {
            keys: ["ArrowDown", "j"],
            description: "Pan down",
            callback: () => camera.pan(0, -panAmount),
        },
        {
            keys: ["ArrowLeft", "h"],
            description: "Pan left",
            callback: () => camera.pan(panAmount, 0),
        },
        {
            keys: ["ArrowRight", "l"],
            description: "Pan right",
            callback: () => camera.pan(-panAmount, 0),
        },
        // Zoom
        {
            keys: ["-"],
            description: "Zoom out",
            callback: () => camera.changeZoom(1 / 1.1),
        },
        {
            keys: ["="],
            description: "Zoom in",
            callback: () => camera.changeZoom(1.1),
        },
        // Display parameters
        {
            keys: ["f"],
            description: "Toggle field orientation",
            callback: () => (fieldOrientation = !fieldOrientation),
        },
        {
            keys: ["i"],
            description: "Toggle ID display format",
            callback: () => (useNumberIds = !useNumberIds),
        },
        // Control
        // {
        //     keys: ["t"],
        //     description: "Test command",
        //     callback: () => testButton.click(),
        // },
        // Layer visibility (programmatically generated)
        // ...Array.from({ length: 9 }, (_, i) => ({
        //     keys: [`${i + 1}`],
        //     description: `Toggle visibility of layer ${i + 1}`,
        //     callback: () => toggleLayerVisibilityByIndex(i + 1),
        // })),
    ];

    // Key handler with support for multiple keys per command
    function handleKeydown(e: KeyboardEvent) {
        const pressedKey = e.key;

        hotkeys.some((hotkey) => {
            if (hotkey.keys.includes(pressedKey)) {
                e.preventDefault();
                hotkey.callback();
                return true; // Stop checking once found
            }
        });
    }

    onMount(() => {
        ctx = canvas.getContext("2d")!;
        resizeCanvas();
        draw();

        window.addEventListener("resize", resizeCanvas);

        window.addEventListener("wheel", (e) => {
            if (e.deltaY > 0) {
                camera.changeZoom(1.03);
            } else {
                camera.changeZoom(1 / 1.03);
            }
        });

        canvas.addEventListener("mousedown", (e) => {
            isDragging = true;
            startX = e.clientX - camera.panX;
            startY = e.clientY - camera.panY;

            if (e.altKey) {
                isBallDragging = true;
            }
            startBallX = startX / (camera.zoom * camera.zoomParam);
            startBallY = startY / (camera.zoom * camera.zoomParam);
            deltaBallX = 0;
            deltaBallY = 0;
        });

        canvas.addEventListener("mousemove", (e) => {
            if (!isDragging) {
                return;
            }

            if (e.altKey) {
                deltaBallX = -(
                    (e.clientX - camera.panX) /
                        (camera.zoom * camera.zoomParam) -
                    startBallX
                );
                deltaBallY = -(
                    (e.clientY - camera.panY) /
                        (camera.zoom * camera.zoomParam) -
                    startBallY
                );
                // console.log(deltaBallX, deltaBallY);
            } else {
                camera.panX = e.clientX - startX;
                camera.panY = e.clientY - startY;
            }
        });

        canvas.addEventListener("mouseup", (e) => {
            if (isDragging && e.altKey) {
                const vx = deltaBallX * velScaleFactor;
                const vy = deltaBallY * velScaleFactor;
                // socket.emit("send_signal", { "larcmacs": "set_ball", "data": { "x": startBallX, "y": -startBallY, "vx": vx, "vy": -vy } });
            }
            isDragging = false;
            isBallDragging = false;
        });

        canvas.addEventListener("mouseleave", () => {
            isDragging = false;
            isBallDragging = false;
        });

        window.addEventListener("keydown", handleKeydown);
    });

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        draw();
    }

    function draw() {
        if (!ctx) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.save();
        ctx.translate(
            canvas_window_center_x + camera.panX,
            canvas_window_center_y + camera.panY,
        );
        ctx.scale(
            camera.zoom * camera.zoomParam,
            camera.zoom * camera.zoomParam,
        );

        const gradient = ctx.createLinearGradient(
            0,
            0,
            canvas.width,
            canvas.height,
        );
        gradient.addColorStop(0, "#1a1a1a");
        gradient.addColorStop(1, "#4a4a4a");

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        drawField(currentDivision, "left");

        ctx.restore();
        requestAnimationFrame(draw);
    }

    function drawField(
        division: "divB" | "divC",
        field_orientation: "left" | "right",
    ) {
        ctx.save();
        if (field_orientation == "left") {
            ctx.scale(-1, 1);
        }
        ctx.drawImage(
            divFields[division],
            -divFields[division].width / 2,
            -divFields[division].height / 2,
        );
        ctx.restore();
    }
</script>

<main>
    <div class="canvas-container">
        <canvas bind:this={canvas}></canvas>
    </div>

    <div
        class="panel right"
        style="
        --card-background-color:#ffffffcc;
        --right-width:{rightWidth}px;
        --right-pos:{showRight ? 0 : -rightWidth}px;
        --panel-bottom:{showBottom ? bottomHeight : 0}px;
        --panel-top:{showTop ? topHeight : 0}px;
    "
    >
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
        <button
            class="button-4 wide"
            onclick={() => {
                console.log("test");
            }}>Test button</button
        >

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

        <hr />

        <h3>Layers</h3>

        <hr />

        <div class="version-info">
            <p><kbd>?</kbd> - Show help</p>
            <p>Version: {currentVersion}</p>
        </div>

        {#if showHelp}
            <div class="help-menu" transition:fade>
                <h3>Hotkeys</h3>
                {#each hotkeys as hotkey}
                    <p>
                        <kbd>
                            {#each hotkey.keys as key, index}
                                {index > 0 ? "/" : ""}{key}
                            {/each}
                        </kbd>
                        - {hotkey.description}
                    </p>
                {/each}
            </div>
        {/if}
    </div>
</main>

<style>
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
        min-height: 100vh; /* or fixed height if needed */
    }

    hr {
        /* flex-grow: 1; */
        width: 100%; /* or this */
    }

    .right {
        top: var(--panel-top);
        bottom: var(--panel-bottom);
        width: var(--right-width);
        right: var(--right-pos);
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
</style>
