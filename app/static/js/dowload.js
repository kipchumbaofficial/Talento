document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.photo-checkbox');
    const downloadSection = document.getElementById('downloadSection');
    //const downloadButton = document.getElementById('downloadButton');
    const selectedCount = document.getElementById('selectedCount');

    let count = 0;

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                count++;
            } else {
                count--;
            }
            selectedCount.textContent = count.toString()

            //Show dowload button if atleast one is selected
            if (count > 0) {
                downloadSection.classList.remove('hidden');
            } else {
                downloadSection.classList.add('hidden');
            }
        });
    });
});

// Show download section if atleast o