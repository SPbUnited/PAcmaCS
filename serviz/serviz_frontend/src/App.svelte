<script lang="ts">
    import UI from "./lib/UI.svelte";
</script>

<main>
    <canvas id="canvas"></canvas>
    <div class="container">
        <div id="canvas-window" class="canvas-window"></div>
        <UI/>
        <script src="/public/scripts/socket.io.js"></script>
        <script src="/public/scripts/script.js"></script>
    </div>
</main>

<style>
</style>
