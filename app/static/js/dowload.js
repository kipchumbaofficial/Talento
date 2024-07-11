document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.photo-checkbox');
    const downloadSection = document.getElementById('downloadSection');
    const selectedCount = document.getElementById('selectedCount');

    let count = 0;
    let totalPrice = 0;
    let selectedPhotos = [];

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const price = parseFloat(this.dataset.price);
            const photo = this.closest('div.relative').querySelector('img').src;
        
            if (this.checked) {
                count++;
                totalPrice += price;
                selectedPhotos.push(photo);
            } else {
                count--;
                totalPrice -= price;
                selectedPhotos = selectedPhotos.filter(p => p !== photo);
            }
            selectedCount.textContent = count.toString()

            //Show dowload button if atleast one is selected
            if (count > 0) {
                downloadSection.classList.remove('hidden');
            } else {
                downloadSection.classList.add('hidden');
            }
            console.log('Selected photos:', selectedPhotos);
        });
    });

    // Handle checkout button click
    document.getElementById('submit').addEventListener('click', function(event) {
        event.preventDefault();

        const checkoutData = {
            price: (totalPrice / count).toFixed(2),
            count: count,
            total: totalPrice.toFixed(2),
            selected_photos: selectedPhotos
        };

        console.log('Checkout data:', checkoutData);
        
        fetch('/prepare_checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(checkoutData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert('Failed to prepare checkout!')
            }
        });
    });
});

