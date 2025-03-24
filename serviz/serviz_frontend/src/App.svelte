<script lang="ts">
    import UI from "./lib/UI.svelte";
</script>

<main>
    <canvas id="canvas"></canvas>
    <div class="container">
        <div id="canvas-window" class="canvas-window"></div>
        <UI/>
    </div>
    <script src="/static/scripts/socket.io.js"></script>
    <script src="/static/scripts/script.js"></script>
</main>

<style>
</style>
