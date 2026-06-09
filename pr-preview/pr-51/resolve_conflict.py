import sys

with open('domain_eci.html', 'r') as f:
    content = f.read()

conflict_start = """<<<<<<< Updated upstream
                <div id="chart-container" class="w-full h-full"></div>
                <div id="breakpoint-stats" class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm p-4 rounded-lg shadow-lg border border-gray-200 text-xs hidden z-10 max-w-xs">
                    <h3 id="stats-title" class="font-bold text-gray-800 mb-2 border-b pb-1">Breakpoint Analysis</h3>
                    <div id="breakpoint-content" class="space-y-1.5 text-gray-600"></div>
======="""

conflict_end = """<<<<<<< Updated upstream
                <div id="chart-container" class="w-full h-full"></div>
                <div id="breakpoint-stats" class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm p-4 rounded-lg shadow-lg border border-gray-200 text-xs hidden z-10 max-w-xs">
                    <h3 id="stats-title" class="font-bold text-gray-800 mb-2 border-b pb-1">Breakpoint Analysis</h3>
                    <div id="breakpoint-content" class="space-y-1.5 text-gray-600"></div>
=======
                <div class="flex-1 p-2 lg:p-6 relative min-h-0">
                    <div id="chart-container" class="w-full h-full"></div>
                </div>
                <div id="breakpoint-stats" class="w-full bg-white border-t border-gray-200 p-4 text-xs hidden z-10 shadow-[0_-4px_12px_rgba(0,0,0,0.05)]">
                    <h3 class="font-bold text-gray-800 mb-2 border-b pb-1 inline-block mr-4">Breakpoint Analysis</h3>
                    <div id="breakpoint-content" class="text-gray-600 inline-block"></div>
>>>>>>> Stashed changes"""

# The full block to search for is defined by the markers
start_marker = "<<<<<<< Updated upstream"
end_marker = ">>>>>>> Stashed changes"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_marker)

    # Replacement block
    replacement = """                <div class="flex-1 p-2 lg:p-6 relative min-h-0">
                    <div id="chart-container" class="w-full h-full"></div>
                </div>
                <div id="breakpoint-stats" class="w-full bg-white border-t border-gray-200 p-4 text-xs hidden z-10 shadow-[0_-4px_12px_rgba(0,0,0,0.05)]">
                    <h3 id="stats-title" class="font-bold text-gray-800 mb-2 border-b pb-1 inline-block mr-4">Breakpoint Analysis</h3>
                    <div id="breakpoint-content" class="text-gray-600 inline-block"></div>
                </div>"""

    new_content = content[:start_idx] + replacement + content[end_idx:]

    with open('domain_eci.html', 'w') as f:
        f.write(new_content)
    print("Conflict resolved.")
else:
    print("Conflict markers not found.")
