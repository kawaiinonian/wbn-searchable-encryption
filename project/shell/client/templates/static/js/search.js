//目前还不知道怎么和后端进行交互返回文件列表
const searchInput = document.querySelector('.search-input');
const searchButton = document.querySelector('.search-button');
const spinner = document.getElementById('spinner');
const loadingAnimation = document.getElementById('loading-animation');

//点击显示加载动画
searchButton.addEventListener('click', function() {
    const query = searchInput.value;

    // spinner.style.display = 'block'; // 开始搜索，显示加载动画
    loadingAnimation.style.display = 'block';

    fetch(`https://your-server.com/api/files?query=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        // spinner.style.display = 'none'; // 搜索结束，隐藏加载动画
        loadingAnimation.style.display = 'none';

        window.location.href = '/results.html';
        localStorage.setItem('fileList', JSON.stringify(data.files));
      })
      .catch(error => {
        // spinner.style.display = 'none'; // 发生错误，隐藏加载动画
        loadingAnimation.style.display = 'none';
        console.error('Error:', error);
      });
  
});

//用来实现点击文件缩小搜索框，点击缩小狂回到原来样式
// 获取元素
var searchImage = document.querySelector('.search-image');
var fileBox = document.querySelector('#files');
var fileList = document.querySelector('.file-list'); 
// 监听文件框的点击事件
fileBox.addEventListener('click', function() {
    searchImage.classList.add('small-search');
    fileList.classList.add('small-files'); // 文件列表也向上移动
});

// 监听搜索框的点击事件
searchImage.addEventListener('click', function() {
    searchImage.classList.remove('small-search');
    fileList.classList.remove('small-files'); // 文件列表返回原位
});



 //搜索框实现功能，前面已经获取到了搜索框中的内容
 searchButton.addEventListener('click', () => {
   // 获取输入框中的搜索关键词
   const searchKeyword = searchInput.value.toLowerCase().trim();
   
   // 获取所有文件元素
   const fileItems = document.querySelectorAll('.file-item');
   
   // 遍历所有文件元素，判断文件名是否包含搜索关键词
   fileItems.forEach(fileItem => {
     const fileName = fileItem.querySelector('.file-link').textContent.toLowerCase();
     if (fileName.includes(searchKeyword)) {
       // 如果包含搜索关键词，则显示该文件元素
       fileItem.style.display = 'flex';
     } else {
       // 否则隐藏该文件元素
       fileItem.style.display = 'none';
     }
   });
 });

 //点击“我已上传”跳转到对应界面
 document.getElementById('uploadButton').addEventListener('click', function(e) {
  e.preventDefault();  // 阻止链接的默认行为
  
  // 弹出确认对话框
  Swal.fire({
    title: 'Are you sure?',
    text: "You want to navigate to another page",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, navigate!'
  }).then((result) => {
    // 如果用户点击了“确认”按钮
    if (result.isConfirmed) {
      window.location.href = '../html/upload.html';
    }
  })
});