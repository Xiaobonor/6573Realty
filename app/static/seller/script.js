// app/static/seller/script.js
document.getElementById('sellerForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const data = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        line: document.getElementById('line').value,
        company: document.getElementById('company').value,
        email: document.getElementById('email').value
    };

    const response = await fetch('/api/v1/seller/register_seller', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (response.ok) {
        alert('Seller registered successfully');
        window.location.href = '/';
    } else {
        alert(`Error: ${result.error}`);
    }
});
