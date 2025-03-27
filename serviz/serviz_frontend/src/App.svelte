<script lang="ts">
    import RightPanel from "./lib/rightPanel.svelte";
    import FieldCanvas from "./lib/FieldCanvas.svelte";

    let showTop = $state(false);
    let showRight = $state(true);
    let showBottom = $state(false);
    let showLeft = $state(false);

    let topHeight = $state(150);
    let rightWidth = $state(200);
    let bottomHeight = $state(150);
    let leftWidth = $state(150);

    let canvas_window = $derived({
            offsetLeft: showLeft ? leftWidth : 0,
            offsetTop: showTop ? topHeight : 0,
            offsetWidth: window.innerWidth - (showLeft ? leftWidth : 0) - (showRight ? rightWidth : 0),
            offsetHeight: window.innerHeight - (showTop ? topHeight : 0) - (showBottom ? bottomHeight : 0),
    });
</script>

<main>

<FieldCanvas {canvas_window} />

<RightPanel
    --card-background-color=#ffffffcc
    --right-width="{rightWidth}px"
    --right-pos="{showRight ? 0 : -rightWidth}px"
    --panel-bottom="{showBottom ? bottomHeight : 0}px"
    --panel-top="{showTop ? topHeight : 0}px"
    bind:width={rightWidth}
    />

</main>

<style>
</style>
