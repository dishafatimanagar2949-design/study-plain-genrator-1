// JS for dynamic subject rows, form management, and user-friendly behavior

function makeSubjectRow(index) {
    const wrapper = document.createElement('div');
    wrapper.className = 'grid gap-3 rounded-xl border border-slate-700 bg-slate-800 p-4 shadow-sm sm:grid-cols-3';

    wrapper.innerHTML = `
        <div class="col-span-1 sm:col-span-1">
            <label class="block text-xs text-slate-300">Subject</label>
            <input name="subject[]" type="text" required placeholder="e.g., Math" class="mt-1 w-full rounded-lg border border-slate-600 bg-slate-900 px-2 py-1 text-sm text-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20" />
        </div>
        <div class="col-span-1 sm:col-span-1">
            <label class="block text-xs text-slate-300">Topic</label>
            <input name="topic[]" type="text" required placeholder="e.g., Algebra" class="mt-1 w-full rounded-lg border border-slate-600 bg-slate-900 px-2 py-1 text-sm text-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20" />
        </div>
        <div class="col-span-1 sm:col-span-1">
            <label class="block text-xs text-slate-300">Difficulty</label>
            <input name="difficulty[]" type="number" min="1" max="5" value="3" required class="mt-1 w-full rounded-lg border border-slate-600 bg-slate-900 px-2 py-1 text-sm text-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20" />
        </div>
        <div class="col-span-1 sm:col-span-1">
            <label class="block text-xs text-slate-300">Performance</label>
            <input name="performance[]" type="number" min="1" max="5" value="3" required class="mt-1 w-full rounded-lg border border-slate-600 bg-slate-900 px-2 py-1 text-sm text-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20" />
        </div>
        <div class="col-span-1 sm:col-span-1">
            <label class="block text-xs text-slate-300">Deadline</label>
            <input name="deadline[]" type="date" required class="mt-1 w-full rounded-lg border border-slate-600 bg-slate-900 px-2 py-1 text-sm text-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20" />
        </div>
        <div class="col-span-1 sm:col-span-1 flex items-end gap-2">
            <div class="w-full">
                <label class="block text-xs text-slate-300">Target Hours</label>
                <input name="hours[]" type="number" step="0.5" min="0.5" value="2" required class="mt-1 w-full rounded-lg border border-slate-600 bg-slate-900 px-2 py-1 text-sm text-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20" />
            </div>
            <button type="button" class="rounded-lg bg-rose-600 px-3 py-2 text-xs font-semibold text-white hover:bg-rose-500" aria-label="Remove subject">Remove</button>
        </div>
    `;

    const removeBtn = wrapper.querySelector('button[aria-label="Remove subject"]');
    if (removeBtn) {
        removeBtn.addEventListener('click', () => wrapper.remove());
    }

    return wrapper;
}

function addSubjectRow() {
    document.getElementById('subjectRows').appendChild(makeSubjectRow());
}

window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('addSubjectBtn').addEventListener('click', addSubjectRow);
    if (document.getElementById('subjectRows').children.length === 0) addSubjectRow();
});

function exportCSV() {
    const rows = [];
    rows.push(['Date', 'Time', 'Subject', 'Topic', 'Hours'].join(','));

    const table = document.querySelector('.data-table');
    if (!table) {
        alert('No timetable to export');
        return;
    }

    table.querySelectorAll('tbody tr').forEach(row => {
        const cells = Array.from(row.querySelectorAll('td')).map(cell => cell.innerText.trim());
        if (cells.length >= 5) rows.push([cells[0], cells[1], cells[2], cells[3], cells[4]].join(','));
    });

    const blob = new Blob([rows.join('\\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'study-plan.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}
