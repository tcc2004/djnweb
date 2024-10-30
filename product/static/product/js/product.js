document.addEventListener('DOMContentLoaded', function() {
    // Hiển thị hoặc ẩn nút xóa khi có checkbox được chọn
    const checkboxes = document.querySelectorAll('.product-checkbox');
    const deleteButton = document.querySelector('.btn-delete');

    function toggleDeleteButton() {
        let isChecked = false;
        checkboxes.forEach(function(checkbox) {
            if (checkbox.checked) {
                isChecked = true;
            }
        });
        deleteButton.style.display = isChecked ? 'block' : 'none';
    }

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', toggleDeleteButton);
    });

    // Xử lý checkbox "Chọn tất cả"
    document.getElementById('select-all').addEventListener('click', function(event) {
        let checkboxes = document.querySelectorAll('.product-checkbox');
        for (let checkbox of checkboxes) {
            checkbox.checked = event.target.checked;
        }
    });

    // Tự động ẩn thông báo sau 5 giây
    setTimeout(function() {
        let messages = document.querySelector('.messages');
        if (messages) {
            messages.style.display = 'none';
        }
    }, 5000);

    // Confirm Delete
    function confirmDelete() {
        return confirm("Bạn có chắc chắn muốn xóa sản phẩm này không?");
    }
    const toggleButton = document.getElementById('toggle-filter');
    const filterForm = document.getElementById('filter-form');

    toggleButton.addEventListener('click', function() {
        // Sử dụng 'display' để kiểm soát việc hiển thị form
        if (filterForm.style.display === 'none') {
            filterForm.style.display = 'block';
        } else {
            filterForm.style.display = 'none';
        }
    });
    // Lặp qua từng sản phẩm để thiết lập đếm ngược và kiểm tra ngày hết hạn
    const productRows = document.querySelectorAll('tr');
    productRows.forEach(function(productRow) {
        const productIdElement = productRow.querySelector('input[name="product_ids"]');
        if (productIdElement) {
            const productId = productIdElement.value;
            const countdownElement = document.getElementById(`countdown-${productId}`);
            const ngayHetHanText = productRow.querySelector('td:nth-child(7)').textContent.trim();
            if (ngayHetHanText) {
                function updateCountdown() {
                    const ngayHetHanDate = new Date(ngayHetHanText);
                    const now = new Date();
                    const timeDifference = ngayHetHanDate - now;
                    if (timeDifference <= 0) {
                        countdownElement.textContent = 'Sản phẩm đã hết hạn.';
                        // deleteButton.style.display = 'inline-block'; // Hiển thị nút "Xóa"
                        return;
                    }
                    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((timeDifference / (1000 * 60 * 60)) % 24);
                    const minutes = Math.floor((timeDifference / (1000 * 60)) % 60);
                    const seconds = Math.floor((timeDifference / 1000) % 60);
                    countdownElement.textContent = `Còn lại: ${days} ngày, ${hours} giờ, ${minutes} phút, ${seconds} giây`;
                    setTimeout(updateCountdown, 1000);
                }
                updateCountdown();
            }
        } else {
            console.warn("Không tìm thấy input với name 'product_ids' trong hàng sản phẩm này.");
        }
    });
});

