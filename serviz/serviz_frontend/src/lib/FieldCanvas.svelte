<script lang="ts">
    import { onMount } from "svelte";

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
        panX: number;
        panY: number;
        zoom: number;
        zoomParam: number;

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
    }

    let { canvas_window } = $props();

    let canvas_window_center_x =
        canvas_window.offsetTop + canvas_window.offsetWidth / 2;
    let canvas_window_center_y =
        canvas_window.offsetLeft + canvas_window.offsetHeight / 2;

    let camera = $state(
        new Camera(canvas_window_center_x, canvas_window_center_y, 1, zoomParams[currentDivision]),
    );

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

    onMount(() => {
        ctx = canvas.getContext("2d")!;
        resizeCanvas();
        draw();

        window.addEventListener("resize", resizeCanvas);

        window.addEventListener("wheel", (e) => {
            if (e.deltaY > 0) {
                camera.zoom *= 1.03;
            } else {
                camera.zoom /= 1.03;
            }
            camera.zoom = Math.min(Math.max(camera.zoom, 0.1), 10);
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

        return () => {
            window.removeEventListener("resize", resizeCanvas);
        };
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
        ctx.translate(camera.panX, camera.panY);
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

<div class="canvas-container">
    <canvas bind:this={canvas}></canvas>
</div>

<style>
    .canvas-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 0;
    }
</style>
