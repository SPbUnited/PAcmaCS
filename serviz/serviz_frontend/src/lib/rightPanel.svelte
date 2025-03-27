<script lang="ts">
    let { width = $bindable() } = $props()
</script>

<div class="panel right">
    <div class="controls">
        <h3>Right Panel</h3>
        <input type="range" bind:value={width} min="150" max="300" />
        <span>Width: {width}px</span>
    </div>
</div>

<style>
    .panel {
        position: fixed;
        background: var(--card-background-color);
        padding: 1rem;
        box-shadow: var(--card-box-shadow);
        z-index: 1;
        transition: all 0.3s ease;
    }

    .right {
        top: var(--panel-top);
        bottom: var(--panel-bottom);
        width: var(--right-width);
        right: var(--right-pos);
    }
</style>