// Mock testing the extraction logic
const inputs = [
    // Case 1: Markdown block
    `Here is the code:
\`\`\`javascript
function getChartConfig(data) {
    return { data: [] };
}
\`\`\`
`,
    // Case 2: Chatty prefix
    `Sure! Here is the function:
function getChartConfig(data) {
    return { data: [] };
}`,
    // Case 3: Just the object (Edge case from legacy code support)
    `return {
    data: [],
    layout: {}
};`
];

inputs.forEach((input, i) => {
    console.log(`--- Test Case ${i + 1} ---`);
    let text = input;
    const mdMatch = text.match(/```(?:javascript|js)?\s*([\s\S]*?)```/);
    if (mdMatch && mdMatch[1]) {
        text = mdMatch[1].trim();
    } else {
        const funcStart = text.indexOf('function getChartConfig');
        if (funcStart !== -1) {
             text = text.substring(funcStart);
        } else {
             if (text.includes('return {')) {
                 text = `function getChartConfig(data) { ${text} }`;
             }
        }
    }

    console.log("Result starts with:", text.substring(0, 50).replace(/\n/g, ' '));
    if (!text.includes('function getChartConfig')) {
        console.error("FAIL: Function not found");
    } else {
        console.log("PASS");
    }
});
