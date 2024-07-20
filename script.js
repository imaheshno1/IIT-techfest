document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const resultsDiv = document.getElementById('results');
    const resultsTable = document.getElementById('results-table').getElementsByTagName('tbody')[0];
    const downloadBtn = document.getElementById('download-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const groupFile = document.getElementById('group-file').files[0];
        const hostelFile = document.getElementById('hostel-file').files[0];

        if (!groupFile || !hostelFile) {
            alert('Please select both CSV files.');
            return;
        }

        const formData = new FormData();
        formData.append('group_file', groupFile);
        formData.append('hostel_file', hostelFile);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Server error');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

    function displayResults(data) {
        resultsTable.innerHTML = '';
        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row['Group ID']}</td>
                <td>${row['Hostel Name']}</td>
                <td>${row['Room Number']}</td>
                <td>${row['Members Allocated']}</td>
            `;
            resultsTable.appendChild(tr);
        });
        resultsDiv.classList.remove('hidden');
    }

    downloadBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/download');
            if (!response.ok) {
                throw new Error('Download failed');
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'allocations.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error:', error);
            alert('Download failed. Please try again.');
        }
    });
});