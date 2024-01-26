

<script>
    document.addEventListener("DOMContentLoaded", function () {
        // Get all elements with the class 'quantity-container'
        var quantityContainers = document.querySelectorAll('.quantity-container');

        // Add click event listeners to the increase and decrease buttons
        quantityContainers.forEach(function (container) {
            var increaseButton = container.querySelector('.increase');
            var decreaseButton = container.querySelector('.decrease');
            var productId = increaseButton.getAttribute('data-product-id');

            increaseButton.addEventListener('click', function () {
                // Call the changeQuantity function with the product ID and change value
                changeQuantity(productId, 1);
            });

            decreaseButton.addEventListener('click', function () {
                // Call the changeQuantity function with the product ID and change value
                changeQuantity(productId, -1);
            });
        });

        // Function to change the quantity via AJAX
        function changeQuantity(productId, change) {
            // Make an AJAX request to the Flask route
            fetch('/change_quantity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'product_id': productId,
                    'change': change,
                }),
            })
            .then(response => {
                // Handle the response if needed
                console.log('Quantity changed successfully');

                // Update the total in the table
                updateTotal(productId);
            })
            .catch(error => {
                console.error('Error changing quantity:', error);
            });
        }

        // Function to update the total in the table
        function updateTotal(productId) {
            // Calculate the new total based on quantity and price
            var quantityInput = document.querySelector(`.quantity-amount[data-product-id="${productId}"]`);
            var price = parseFloat(quantityInput.getAttribute('data-price'));
            var newQuantity = parseInt(quantityInput.value);
            var newTotal = price * newQuantity;

            // Update the total in the table
            var totalCell = document.querySelector(`td[data-total-id="${productId}"]`);
            totalCell.textContent = `$${newTotal.toFixed(2)}`;

            // Calculate and update the overall cart total
            calculateCartTotal();
        }

        // Function to calculate the overall cart total and update the displayed total
        function calculateCartTotal() {
            var totalCells = document.querySelectorAll('td[data-total-id]');
            var overallTotal = Array.from(totalCells).reduce(function (acc, totalCell) {
                return acc + parseFloat(totalCell.textContent.replace('$', ''));
            }, 0.0);

            // Update the displayed total
            var cartTotalElement = document.getElementById('cart-total');
            if (cartTotalElement) {
                cartTotalElement.textContent = `$${overallTotal.toFixed(2)}`;
            }
        }
    });
</script>

<script>
    document.addEventListener("DOMContentLoaded", function () {
        var removeButtons = document.querySelectorAll('.remove-button');

        removeButtons.forEach(function (button) {
            var productId = button.getAttribute('data-product-id');

            button.addEventListener('click', function () {
                // Call the removeProduct function with the product ID
                removeProduct(productId);
            });
        });

      function removeProduct(productId) {
    // Make an AJAX request to the Flask route
    fetch('/remove_from_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'product_id': productId,
        }),
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        // Handle the response data
        if (data.status === 'success') {
            console.log('Product removed successfully');
            // Update the total in the table
            updateTotal(productId);
        } else {
            console.error('Error removing product:', data.status);
        }
    })
    .catch(error => {
        console.error('Error removing product:', error);
    });
}

        // Function to update the total in the table
        function updateTotal(productId) {
            // Calculate the new total based on quantity and price
            var quantityInput = document.querySelector(`.quantity-amount[data-product-id="${productId}"]`);
            var price = parseFloat(quantityInput.getAttribute('data-price'));
            var newQuantity = parseInt(quantityInput.value);
            var newTotal = price * newQuantity;

            // Update the total in the table
            var totalCell = document.querySelector(`td[data-total-id="${productId}"]`);
            totalCell.textContent = `$${newTotal.toFixed(2)}`;

            // Calculate and update the overall cart total
            calculateCartTotal();
        }

    });
</script>

<script>
    document.addEventListener("DOMContentLoaded", function () {
        // Function to update the cart counter via AJAX
        function updateCartCounter() {
            // Make an AJAX request to the Flask route
            fetch('/cart_count')
                .then(response => response.json())
                .then(data => {
                    // Update the cart counter
                    var counter = document.getElementById('cart-counter');
                    counter.textContent = data.count;
                })
                .catch(error => {
                    console.error('Error updating cart counter:', error);
                });
        }

        // Update the cart counter on page load
        updateCartCounter();

        // You can also call this function whenever an item is added or removed from the cart
    });
</script>


<script>
    document.addEventListener("DOMContentLoaded", function () {
        // Function to update the cart counter via AJAX
        function updateCartCounter() {
            // Make an AJAX request to the Flask route
            fetch('/cart_count')
                .then(response => response.json())
                .then(data => {
                    // Update the cart counter
                    var counter = document.getElementById('cart-counter');
                    counter.textContent = data.count;
                })
                .catch(error => {
                    console.error('Error updating cart counter:', error);
                });
        }

        // Update the cart counter on page load
        updateCartCounter();

        // You can also call this function whenever an item is added or removed from the cart
    });
</script>