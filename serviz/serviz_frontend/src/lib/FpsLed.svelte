<script>
    import Led from "./Led.svelte";

    let buffer = [];
    const alpha = 0.3;
    let filteredDt = $state(0);
    let color = $state("#000000");

    export function addDt(dt) {
      filteredDt = alpha * filteredDt + (1 - alpha) * dt;
    }

    const good = 20;
    const norm = 25;
    const ok = 30;
    const bad = 50;
    const worst = 100;

    function getColor(dt) {
      let r, g, b;
      if (dt <= good) {
        [r, g, b] = [0, 255, 0]; // Green
      } else if (dt <= norm) {
        const factor = (dt - good) / 3;
        r = Math.round(255 * factor);
        g = 255;
        b = 0;
      } else if (dt <= ok) {
        [r, g, b] = [255, 255, 0]; // Yellow
      } else if (dt <= bad) {
        const factor = (dt - ok) / norm;
        r = 255;
        g = Math.round(255 * (1 - factor));
        b = 0;
      } else if (dt <= worst) {
        const factor = (dt - bad) / bad;
        r = Math.round(255 * (1 - factor));
        g = 0;
        b = 0;
      } else {
        [r, g, b] = [0, 0, 0]; // Black
      }
      return `rgb(${r},${g},${b})`;
    }

    $effect(() => {
      color = getColor(filteredDt);
    });

  </script>

<Led bind:color/>
