// // Hàm xác nhận khi xóa danh mục
// function confirmDelete() {
//     return confirm("Bạn có chắc chắn muốn xóa danh mục này không?");
// }

// // Tự động ẩn thông báo sau 5 giây
// setTimeout(function() {
//     let messages = document.querySelector('.messages');
//     if (messages) {
//         messages.style.display = 'none';
//     }
// }, 5000); // 5000ms = 5 giây

// // Xử lý checkbox "Chọn tất cả"
// document.getElementById('select-all').addEventListener('click', function(event) {
//     let checkboxes = document.querySelectorAll('.category-checkbox');
//     for (let checkbox of checkboxes) {
//         checkbox.checked = event.target.checked;
//     }
// });

// // Lấy tất cả các checkbox và nút xóa
// const checkboxes = document.querySelectorAll('.category-checkbox');
// const deleteButton = document.querySelector('.btn-delete');

// // Hàm kiểm tra nếu có checkbox nào được chọn
// function toggleDeleteButton() {
//     let isChecked = false;

//     // Kiểm tra nếu có ít nhất một checkbox được chọn
//     checkboxes.forEach(function(checkbox) {
//         if (checkbox.checked) {
//             isChecked = true;
//         }
//     });

//     // Hiển thị nút xóa nếu có checkbox nào được chọn
//     if (isChecked) {
//         deleteButton.style.display = 'block';  // Hiển thị nút xóa
//     } else {
//         deleteButton.style.display = 'none';  // Ẩn nút xóa nếu không checkbox nào được chọn
//     }
// }

// // Thêm sự kiện "change" để kiểm tra mỗi lần có sự thay đổi ở checkbox
// checkboxes.forEach(function(checkbox) {
//     checkbox.addEventListener('change', toggleDeleteButton);
// });
