//目前还不知道怎么和后端进行交互返回文件列表
const searchInput = document.querySelector('.search-input');
const searchButton = document.querySelector('.search-button');
const spinner = document.getElementById('spinner');
const loadingAnimation = document.getElementById('loading-animation');

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




