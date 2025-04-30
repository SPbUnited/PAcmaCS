<script lang="ts">
    let { raw_telemetry = $bindable() }: { raw_telemetry: string } = $props();

    function format_telemetry(text: string): string {
        if(!text)
            return text;

        const style = `
<style>
    /* Scoped styles that only affect elements within .tq (telemetry output) */
    .tq r {
        color: red;
    }
    .tq o {
        color: orange;
    }
    .tq y {
        color: yellow;
    }
    .tq g {
        color: green;
    }
    .tq b {
        color: blue;
    }
    .tq p {
        color: purple;
    }
    .tq k {
        color: black;
    }
    .tq w {
        color: white;
    }
    .tq c {
        color: cyan;
    }
    .tq m {
        color: magenta;
    }
    .tq l {
        color: lime;
    }
    .tq a {
        color: aqua;
    }
    .tq n {
        color: navy;
    }
    .tq v {
        color: violet;
    }
    .tq s {
        color: silver;
    }

    .tq x {
        font-weight: bold;
    }
    .tq i {
        font-style: italic;
    }
    .tq u {
        text-decoration: underline;
    }
    .tq q {
        text-decoration: line-through;
    }
</style>
`;
        // // Mapping of markdown emoji symbols to HTML Unicode entities
        // const emojiMap: Record<string, string> = {
        //     ':smile:': '&#x1F604;',
        //     ':grinning:': '&#x1F600;',
        //     ':heart:': '&#x2764;',
        //     ':thumbsup:': '&#x1F44D;',
        //     ':warning:': '&#x26A0;',
        //     ':rocket:': '&#x1F680;',
        //     ':star:': '&#x2B50;',
        //     ':fire:': '&#x1F525;',
        //     // Add more mappings as needed
        // };

        // // Sort keys by descending length to prioritize longer matches
        // const keys = Object.keys(emojiMap).sort((a, b) => b.length - a.length);

        // // Create regex-safe pattern by escaping special characters
        // const escapedKeys = keys
        //     .map(key => key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
        //     .join('|');

        // // Create regular expression to match all emoji symbols
        // const regex = new RegExp(`(${escapedKeys})`, 'g');

        // Replace matches with corresponding HTML entities
        return style + text; //.replace(regex, (match) => emojiMap[match]);
    }
</script>

<pre>
<code class="tq">
{@html format_telemetry(raw_telemetry)}
</code>
</pre>

