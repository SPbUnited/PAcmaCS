<script lang="ts">
    let { color = $bindable() } = $props();
</script>

<div class="led" style:background-color={color}></div>

<style>
    .led {
        width: 0.8rem;
        height: 0.8rem;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
        transition: background-color 0.1s ease;
    }
</style>