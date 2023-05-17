// 需要优化的的地方搜索 “优化”即可









// 实现文件按钮的所有功能,以实现删除,下载，优化
function FileButtonFunctions(){

    //删除按钮,点击后弹出是否确认删除
    const deleteButtons = document.querySelectorAll(".delete");
  
    deleteButtons.forEach(button => {
      button.addEventListener("click", () => {
        // 获取该文件元素
        const fileItem = button.closest(".file-item");
        //弹出确认删除按钮
        const confirmDelete = confirm("Are you sure you want to delete this file?");
        // 从file-list中删除该文件元素
        if (confirmDelete) {
          fileItem.parentNode.removeChild(fileItem);
        }
      });
    });
  
  // 获取所有下载按钮
  const downloadButtons = document.querySelectorAll(".download");
  
  downloadButtons.forEach(button => {
    button.addEventListener("click", () => {
      // 获取该文件元素
      const fileItem = button.closest(".file-item");
      // 获取文件名和文件内容
      const fileName = fileItem.querySelector(".file-link").textContent;
      const fileContent = "This is the content of file: " + fileName;
      // 弹出确认下载对话框
      const confirmDownload = confirm("Are you sure you want to download " + fileName + "?");
      // 如果确认下载，则创建一个Blob对象并下载,要小心这里只是简单创建了一个blod对象,实际还有其他文件类型,后需完善
      if (confirmDownload) {
        const blob = new Blob([fileContent], { type: "text/plain" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      }
    });
  });
  
  
  //点击分享按钮出现分享面板
  // 创建分享面板
  const sharePanel = document.createElement('div');
  sharePanel.className = 'share-panel';
  sharePanel.innerHTML = `
    <i class="fab fa-weixin"></i>
    <i class="fab fa-qq"></i>
    <i class="fab fa-weibo"></i>
    <i class="fas fa-users"></i> <!-- 朋友圈图标 -->
    <i class="fas fa-globe"></i> <!-- QQ空间图标 -->
  `;
  
  const shareBtns = document.getElementsByClassName('share');
  
  let hideTimeout;
  
  for(let btn of shareBtns) {
    btn.addEventListener('mouseenter', function() {
      clearTimeout(hideTimeout); // 取消之前的隐藏计时器
      btn.parentNode.appendChild(sharePanel);
      sharePanel.classList.add('show');
    });
  
    btn.addEventListener('mouseleave', function() {
      hideTimeout = setTimeout(function() { // 设置隐藏计时器
        sharePanel.classList.remove('show');
        setTimeout(function() {
          if (!sharePanel.classList.contains('show')) {
            btn.parentNode.removeChild(sharePanel);
          }
        }, 500);
      }, 300); // 在鼠标离开后 300ms 再隐藏面板
    });
  }
  
  sharePanel.addEventListener('mouseenter', function() {
    clearTimeout(hideTimeout); // 当鼠标移动到面板上时，取消隐藏计时器
  });
  
  sharePanel.addEventListener('mouseleave', function() {
    hideTimeout = setTimeout(function() { // 当鼠标离开面板时，开始隐藏计时器
      sharePanel.classList.remove('show');
      setTimeout(function() {
        if (!sharePanel.classList.contains('show')) {
          sharePanel.parentNode.removeChild(sharePanel);
        }
      }, 500);
    }, 300);
  });
  
                  }
  
  
  
  // 以上分割线///////////////////////////////////////////////////////////////////////////////////////////////////////
  // 移动到顶部快捷按钮
  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
  
  // Initialize event listeners
  function initEventListeners() {
    var mobileNavBtn = document.querySelector(".mobile-nav-btn");
    mobileNavBtn.addEventListener("click", toggleMobileNav);
  
    var scrollTopBtn = document.querySelector(".scroll-top");
    scrollTopBtn.addEventListener("click", scrollToTop);
  
    // Add scroll event listener to show or hide scroll-to-top button
    window.addEventListener("scroll", function () {
      var scrollTopBtn = document.querySelector(".scroll-top");
      if (window.pageYOffset > 200) {
        scrollTopBtn.style.display = "block";
      } else {
        scrollTopBtn.style.display = "none";
      }
    });
  }
  
  // Initialize the event listeners when DOM is ready
  document.addEventListener("DOMContentLoaded", function () {
    initEventListeners();
  });
  
  // 获取文件的后缀名从而在创建文件和上传文件时来修改图标
  function getFileType(fileName) {
    // 获取文件名中最后一个 "." 的索引
    const dotIndex = fileName.lastIndexOf(".");
    // 如果 "." 不存在，则返回空字符串
    if (dotIndex === -1) {
      return "aaa";
    }
    // 获取文件名的后缀名
    const fileExt = fileName.slice(dotIndex + 1);
    // 根据文件后缀名返回相应的文件类型
    switch (fileExt.toLowerCase()) {
      case "doc":
      case "docx":
        return "word";
      case "pdf":
        return "pdf";
      case "zip":
      case "rar":
        return "archive";
      case "exe":
      case "msi":
        return "exe";
      case "mp4":
        return "mp4";
      case "mp3":
        return "mp3"
      case "jpg":
      case "png":
        return "image"
      case "txt":
        return "txt"
      default:
        return "aaa";
    }
  }
  
  
  
  // 实现文件的新建
  const newBtn = document.getElementById('new-btn');
  const fileList = document.getElementById('files');
  
  // 给新建按钮添加点击事件,新建文件夹，优化，文件夹图标加载不出来
  newBtn.addEventListener('click', () => {
    const fileName = prompt('请输入文件夹名称：'); // 弹出重命名窗口并获取用户输入
  
    if (fileName) { // 如果用户输入了名称
      const newFolder = document.createElement('li');
      newFolder.className = 'file-item';
  
      const fileIcon = document.createElement('div');
      fileIcon.className = 'file-icon';
      const fileIconImg = document.createElement('i');
  
      const lastName=getFileType(fileName);
  
      if(lastName=="word"){
        fileIconImg.className = "fas fa-file-word";
      }
      else if(lastName=="pdf"){
        fileIconImg.className = "fas fa-file-pdf";
      }
      else if(lastName=="txt"){
        fileIconImg.className = "fas fa-file";
      }
      else if(lastName=="mp3"){
        fileIconImg.className = "fas fa-file-audio";
      }
      else if(lastName=="mp4"){
        fileIconImg.className = "fas fa-file-video";
      }
      else if(lastName=="image"){
        fileIconImg.className = "fas fa-file-image";
      }
      else if(lastName=="archive"){
        fileIconImg.className = "fas fa-file-archive";
      }
      else if(lastName=="exe"){
        fileIconImg.className = "fas fa-file-code";
      }
      else if(lastName=="aaa"){
        fileIconImg.className = "fas fa-folder";
      }
     
  
      fileIcon.appendChild(fileIconImg);
      newFolder.appendChild(fileIcon);
  
  
      // 创建文件名和链接,添加文件到列表
      const fileInfo = document.createElement('div');
      fileInfo.className = 'file-info';
      const fileLink = document.createElement('span');
      fileLink.className = 'file-link';
      fileLink.textContent = fileName;
      fileInfo.appendChild(fileLink);
      newFolder.appendChild(fileInfo);
  
  
  
  
  
      // 创建删除、下载和分享,收藏按钮
      // 添加按钮授权
      const authBtn = document.createElement("button");
      authBtn.className = "authorize file-action";
      authBtn.id = 'new-btn';
      const authIcon = document.createElement("i");
      authIcon.className = "fas fa-user-shield";
      authBtn.appendChild(authIcon);
      newFolder.appendChild(authBtn);
  
      const deleteBtn = document.createElement('button');
      deleteBtn.className = 'delete file-action';
      deleteBtn.id = 'new-btn'; // 设置按钮的id
      const deleteIcon = document.createElement('i');
      deleteIcon.className = 'fas fa-trash-alt';
      deleteBtn.appendChild(deleteIcon);
      newFolder.appendChild(deleteBtn);
  
      const downloadBtn = document.createElement('button');
      downloadBtn.className = 'download file-action';
      downloadBtn.id = 'new-btn';
      const downloadIcon = document.createElement('i');
      downloadIcon.className = 'fas fa-download';
      downloadBtn.appendChild(downloadIcon);
      newFolder.appendChild(downloadBtn);
  
      const shareBtn = document.createElement('button');
      shareBtn.className = 'share file-action';
      shareBtn.id = 'new-btn';
      const shareIcon = document.createElement('i');
      shareIcon.className = 'fas fa-share';
      shareBtn.appendChild(shareIcon);
      newFolder.appendChild(shareBtn);
  
      const favoriteBtn = document.createElement('button');
      favoriteBtn.className = 'favorrite file-action';
      favoriteBtn.id = 'new-btn';
      const favoriteIcon = document.createElement('i');
      favoriteIcon.className = 'fas fa-star';
      favoriteBtn.appendChild(favoriteIcon);
      newFolder.appendChild(favoriteBtn);
  
      
      fileList.appendChild(newFolder); // 将文件夹添加到file-list中
    }
  
    //实现新建文件的按钮功能
    // 获取所有删除按钮
    FileButtonFunctions();
    
  });
  
  // 上传文件
  
  
  
  document.getElementById("file-input").addEventListener("change", function (event) {
    const file = event.target.files[0];
  
    if (file) {
      const fileName = file.name;
  
  
      const newFileItem = document.createElement("li");
      newFileItem.className = "file-item";
  
      const fileIcon = document.createElement("div");
      fileIcon.className = "file-icon";
      const fileIconImg = document.createElement("i");
      // 根据文件类型设置图标
     
  
      const lastName=getFileType(fileName);
  
      if(lastName=="word"){
        fileIconImg.className = "fas fa-file-word";
      }
      else if(lastName=="pdf"){
        fileIconImg.className = "fas fa-file-pdf";
      }
      else if(lastName=="txt"){
        fileIconImg.className = "fas fa-file";
      }
      else if(lastName=="mp3"){
        fileIconImg.className = "fas fa-file-audio";
      }
      else if(lastName=="mp4"){
        fileIconImg.className = "fas fa-file-video";
      }
      else if(lastName=="image"){
        fileIconImg.className = "fas fa-file-image";
      }
      else if(lastName=="archive"){
        fileIconImg.className = "fas fa-file-archive";
      }
      else if(lastName=="exe"){
        fileIconImg.className = "fas fa-file-code";
      }
      else if(lastName=="aaa"){
        fileIconImg.className = "fas fa-folder";
      }
  
      fileIcon.appendChild(fileIconImg);
      newFileItem.appendChild(fileIcon);
  
      const fileInfo = document.createElement("div");
      fileInfo.className = "file-info";
      const fileLink = document.createElement("span");
      fileLink.className = "file-link";
      fileLink.textContent = fileName;
      fileInfo.appendChild(fileLink);
  
  
  
      newFileItem.appendChild(fileInfo);
  
      // 添加按钮授权
      const authBtn = document.createElement("button");
      authBtn.className = "authorize file-action";
      authBtn.id = 'new-btn';
      const authIcon = document.createElement("i");
      authIcon.className = "fas fa-user-shield";
      authBtn.appendChild(authIcon);
      newFileItem.appendChild(authBtn);
  
      // 添加删除按钮
      const deleteBtn = document.createElement("button");
      deleteBtn.className = "delete file-action";
      deleteBtn.id = 'new-btn';
      const deleteIcon = document.createElement("i");
      deleteIcon.className = "fas fa-trash-alt";
      deleteBtn.appendChild(deleteIcon);
      newFileItem.appendChild(deleteBtn);
  
      // 添加下载按钮
      const downloadBtn = document.createElement("button");
      downloadBtn.className = "download file-action";
      downloadBtn.id = 'new-btn';
      const downloadIcon = document.createElement("i");
      downloadIcon.className = "fas fa-download";
      downloadBtn.appendChild(downloadIcon);
      newFileItem.appendChild(downloadBtn);
  
      // 添加分享按钮
      const shareBtn = document.createElement("button");
      shareBtn.className = "share file-action";
      shareBtn.id = 'new-btn';
      const shareIcon = document.createElement("i");
      shareIcon.className = "fas fa-share";
      shareBtn.appendChild(shareIcon);
      newFileItem.appendChild(shareBtn);
  
      // 添加收藏按钮
      const favoriteBtn = document.createElement("button");
      favoriteBtn.className = "favorite file-action";
      favoriteBtn.id = 'new-btn';
      const favoriteIcon = document.createElement("i");
      favoriteIcon.className = "fas fa-star";
      favoriteBtn.appendChild(favoriteIcon);
      newFileItem.appendChild(favoriteBtn);
  
      document.getElementById("files").appendChild(newFileItem);
    }
    FileButtonFunctions();
  });
  
  
  
  
  
  
  //排序按键
  const sortSelect = document.getElementById('sort-select');
  const filesList = document.getElementById('files');
  
  sortSelect.addEventListener('change', () => {
    const sortValue = sortSelect.value;
  
    // 对文件列表进行排序
    switch (sortValue) {
      case 'name-asc':
        sortByNameAsc(filesList);
        break;
      case 'name-desc':
        sortByNameDesc(filesList);
        break;
      case 'size-asc':
        sortBySizeAsc(filesList);
        break;
      case 'size-desc':
        sortBySizeDesc(filesList);
        break;
      case 'date-asc':
        sortByDateAsc(filesList);
        break;
      case 'date-desc':
        sortByDateDesc(filesList);
        break;
      default:
        break;
    }
  });
  //字母升序
  function sortByNameAsc(filesList) {
    const items = Array.from(filesList.children);
    items.sort((a, b) => {
      const aName = a.querySelector('.file-link').textContent.toLowerCase();
      const bName = b.querySelector('.file-link').textContent.toLowerCase();
      if (aName < bName) {
        return -1;
      } else if (aName > bName) {
        return 1;
      } else {
        return 0;
      }
    });
    items.forEach(item => {
      filesList.appendChild(item);
    });
  }
  //降序
  function sortByNameDesc(filesList) {
    const items = Array.from(filesList.children);
    items.sort((a, b) => {
      const aName = a.querySelector('.file-link').textContent.toLowerCase();
      const bName = b.querySelector('.file-link').textContent.toLowerCase();
      if (aName > bName) {
        return -1;
      } else if (aName < bName) {
        return 1;
      } else {
        return 0;
      }
    });
    items.forEach(item => {
      filesList.appendChild(item);
    });
  }
  
  
  
  
  
  
                
  // 获取输入框和搜索按钮元素
  const searchInput = document.querySelector('.search-input');
  const searchButton = document.querySelector('.search-button');
  
  //搜索框实现功能
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
  
  
  
  
  
  
  
  
  
  
  
  
  
  