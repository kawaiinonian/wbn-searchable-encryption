//目前还不知道怎么和后端进行交互返回文件列表
const searchInput = document.querySelector('.search-input');
const searchButton = document.querySelector('.search-button');
const spinner = document.getElementById('spinner');
const loadingAnimation = document.getElementById('loading-animation');

// //点击显示加载动画
// searchButton.addEventListener('click', function () {
//   const query = searchInput.value;

//   // spinner.style.display = 'block'; // 开始搜索，显示加载动画
//   loadingAnimation.style.display = 'block';

//   fetch(`https://your-server.com/api/files?query=${encodeURIComponent(query)}`)
//     .then(response => response.json())
//     .then(data => {
//       // spinner.style.display = 'none'; // 搜索结束，隐藏加载动画
//       loadingAnimation.style.display = 'none';

//       window.location.href = '/results.html';
//       localStorage.setItem('fileList', JSON.stringify(data.files));
//     })
//     .catch(error => {
//       // spinner.style.display = 'none'; // 发生错误，隐藏加载动画
//       loadingAnimation.style.display = 'none';
//       console.error('Error:', error);
//     });

// });

//用来实现点击文件缩小搜索框，点击缩小狂回到原来样式
// 获取元素
var searchImage = document.querySelector('.search-image');
var fileBox = document.querySelector('#files');
var fileList = document.querySelector('.file-list');
// 监听文件框的点击事件
fileBox.addEventListener('click', function () {
  searchImage.classList.add('small-search');
  fileList.classList.add('small-files'); // 文件列表也向上移动
});

// 监听搜索框的点击事件
searchImage.addEventListener('click', function () {
  searchImage.classList.remove('small-search');
  fileList.classList.remove('small-files'); // 文件列表返回原位
});


// 实现文件按钮的所有功能,以实现授权、删除,下载，后续调用
function FileButtonFunctions() {

  const authorizeButtons = document.querySelectorAll(".authorize");

  authorizeButtons.forEach(button => {
    button.addEventListener("click", async () => {
      // 使用Fetch API获取用户名列表
      const response = await fetch('/get_usernames/', {
        method: 'GET',
      });

      const data = await response.json();

      if (data.usernames && data.usernames.length > 0) {
        // 构建下拉列表的选项
        const usernames = data.usernames;
        const inputOptions = {};
        usernames.forEach((username, index) => {
          inputOptions[index] = username;
        });

        Swal.fire({
          title: 'Choose a user to authorize:',
          input: 'select',
          inputOptions: inputOptions,
          showCancelButton: true,
          showCloseButton: true,
          focusConfirm: false,
          confirmButtonText: 'Authorize',
        }).then(async (result) => {
          if (result.isConfirmed) {
            const selectedIndex = result.value;
            if (selectedIndex != null) {
              const selectedUsername = usernames[selectedIndex];
              // 获取该文件元素
              const fileItem = button.closest(".file-item");
              const filename = fileItem.querySelector(".file-link").textContent;

              // 向后端发送选中的用户名和文件名
              const formData = new FormData();
              formData.append('username', selectedUsername);
              formData.append('documents', filename);

              const response = await fetch('/offline_auth/', {
                method: 'POST',
                body: formData,
              });

              const data = await response.json();

              if (data.error == '0') {
                // 在前端进行一些成功授权的处理，比如显示成功授权的提示信息
                Swal.fire(
                  'Authorized!',
                  `File ${filename} has been authorized to ${selectedUsername}.`,
                  'success'
                );
              } else {
                // 处理授权失败的情况，比如显示授权失败的提示信息
                Swal.fire(
                  'Authorization Failed!',
                  'Failed to authorize the file.',
                  'error'
                );
              }
            }
          }
        });
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

      Swal.fire({
        title: 'Do you want to download?',
        text: "You are about to download " + fileName + ".",
        icon: 'info',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, download it!'
      }).then((result) => {
        // 如果确认下载，则创建一个Blob对象并下载,要小心这里只是简单创建了一个blod对象,实际还有其他文件类型,后需完善
        if (result.isConfirmed) {
          const blob = new Blob([fileContent], { type: "text/plain" });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = fileName;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
          Swal.fire(
            'Downloaded!',
            'Your file has been downloaded.',
            'success'
          )
        }
      });
    });
  });

  //点击分享按钮出现分享面板
  // 创建分享面板
  const shareButtons = document.querySelectorAll(".share");

  shareButtons.forEach(button => {
    button.addEventListener("click", () => {
      Swal.fire({
        title: 'Share this file',
        html: `
          <div class="share-panel">
            <i class="fab fa-weixin"></i>
            <i class="fab fa-qq"></i>
            <i class="fab fa-weibo"></i>
            <i class="fas fa-users"></i> <!-- 朋友圈图标 -->
            <i class="fas fa-globe"></i> <!-- QQ空间图标 -->
          </div>
        `,
        showConfirmButton: false,
      })
    });
  });
}

FileButtonFunctions();

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
    case "md":
      return "txt"
    default:
      return "aaa";
  }
}


//搜索框实现功能，前面已经获取到了搜索框中的内容
searchButton.addEventListener('click', async () => {
  // 获取输入框中的搜索关键词
  const searchKeyword = searchInput.value.toLowerCase().trim();

  const formData = new FormData();
  formData.append('word', searchKeyword);

  var data;

  try {
    // 使用 fetch API 发送数据
    const response = await fetch('/search/', {
      method: 'POST',
      body: formData,
    });
    data = await response.json();

    if (data['error'] == '1') {
      // 如果服务器返回了一个错误，你可以在这里处理它
      const message = data['msg'];
      Swal.fire(
        'Search Failed!',
        data['msg'],
        'error'
      );
    }
  } catch (error) {
    console.error("error when sending data: ", error);
  }

  const fileNames = data['documents'];

  if (fileNames) {
    const fileListContainer = document.getElementById('files');

    // 在添加新文件之前，清空fileListContainer的内容
    while (fileListContainer.firstChild) {
      fileListContainer.removeChild(fileListContainer.firstChild);
    }

    fileNames.forEach((fileName) => {
      const newfile = document.createElement('li');
      newfile.className = 'file-item';

      const fileIcon = document.createElement('div');
      fileIcon.className = 'file-icon';
      const fileIconImg = document.createElement('i');

      const lastName = getFileType(fileName);

      if (lastName == "word") {
        fileIconImg.className = "fas fa-file-word";
      } else if (lastName == "pdf") {
        fileIconImg.className = "fas fa-file-pdf";
      } else if (lastName == "txt") {
        fileIconImg.className = "fas fa-file-alt";
      } else if (lastName == "mp3") {
        fileIconImg.className = "fas fa-file-audio";
      } else if (lastName == "mp4") {
        fileIconImg.className = "fas fa-file-video";
      } else if (lastName == "image") {
        fileIconImg.className = "fas fa-file-image";
      } else if (lastName == "archive") {
        fileIconImg.className = "fas fa-file-archive";
      } else if (lastName == "exe") {
        fileIconImg.className = "fas fa-file-code";
      } else if (lastName == "aaa") {
        fileIconImg.className = "fas fa-file-alt";
      }

      fileIcon.appendChild(fileIconImg);
      newfile.appendChild(fileIcon);

      // 创建文件名和链接,添加文件到列表
      const fileInfo = document.createElement('div');
      fileInfo.className = 'file-info';
      const fileLink = document.createElement('span');
      fileLink.className = 'file-link';
      fileLink.textContent = fileName;
      fileInfo.appendChild(fileLink);
      newfile.appendChild(fileInfo);

      // 创建删除、下载和分享,收藏按钮
      // 添加按钮授权
      const authBtn = document.createElement("button");
      authBtn.className = "authorize file-action";
      authBtn.id = 'new-btn';
      const authIcon = document.createElement("i");
      authIcon.className = "fas fa-user-shield";
      authBtn.appendChild(authIcon);
      newfile.appendChild(authBtn);

      const downloadBtn = document.createElement('button');
      downloadBtn.className = 'download file-action';
      downloadBtn.id = 'new-btn';
      const downloadIcon = document.createElement('i');
      downloadIcon.className = 'fas fa-download';
      downloadBtn.appendChild(downloadIcon);
      newfile.appendChild(downloadBtn);

      const shareBtn = document.createElement('button');
      shareBtn.className = 'share file-action';
      shareBtn.id = 'new-btn';
      const shareIcon = document.createElement('i');
      shareIcon.className = 'fas fa-share';
      shareBtn.appendChild(shareIcon);
      newfile.appendChild(shareBtn);

      fileListContainer.appendChild(newfile);

      FileButtonFunctions();
    });
  }


  //  // 获取所有文件元素
  //  const fileItems = document.querySelectorAll('.file-item');

  //  // 遍历所有文件元素，判断文件名是否包含搜索关键词
  //  fileItems.forEach(fileItem => {
  //    const fileName = fileItem.querySelector('.file-link').textContent.toLowerCase();
  //    if (fileName.includes(searchKeyword)) {
  //      // 如果包含搜索关键词，则显示该文件元素
  //      fileItem.style.display = 'flex';
  //    } else {
  //      // 否则隐藏该文件元素
  //      fileItem.style.display = 'none';
  //    }
  //  });
});

//点击“我已上传”跳转到对应界面
document.getElementById('uploadButton').addEventListener('click', function (e) {
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
      window.location.href = '../upload';
    }
  })
});

document.getElementById('onlineButton').addEventListener('click', async function (e) {
  e.preventDefault();  // 阻止链接的默认行为

  // 使用Fetch API获取用户名列表
  const response = await fetch('/online_revo/', {
    method: 'GET',
  });

  const data = await response.json();

  if (data.usernames && data.usernames.length > 0) {
    // 构建下拉列表的选项
    const usernames = data.usernames;
    const inputOptions = {};
    usernames.forEach((username, index) => {
      inputOptions[index] = username;
    });

    Swal.fire({
      title: 'Choose a user to revocate:',
      input: 'select',
      inputOptions: inputOptions,
      showCancelButton: true,
      showCloseButton: true,
      focusConfirm: false,
      confirmButtonText: 'Revocate',
    }).then(async (result) => {
      if (result.isConfirmed) {
        const selectedIndex = result.value;
        if (selectedIndex != null) {
          const selectedUsername = usernames[selectedIndex];

          const formData = new FormData();
          formData.append('username', selectedUsername);

          const response = await fetch('/online_revo/', {
            method: 'POST',
            body: formData,
          });

          const data = await response.json();

          if (data.error == '0') {
            Swal.fire(
              'Revocated!',
              `User ${selectedUsername}'s authorization has been revocated.`,
              'success'
            );
          } else {
            Swal.fire(
              'Revocation Failed!',
              'Failed to revocate.',
              'error'
            );
          }
        }
      }
    });
  }
});

document.getElementById('offlineButton').addEventListener('click', async function (e) {
  e.preventDefault();  // 阻止链接的默认行为

  // 使用Fetch API获取用户名列表
  const response = await fetch('/offline_revo/', {
    method: 'GET',
  });

  const data = await response.json();

  if (data.usernames && data.usernames.length > 0) {
    // 构建下拉列表的选项
    const usernames = data.usernames;
    const inputOptions = {};
    usernames.forEach((username, index) => {
      inputOptions[index] = username;
    });

    Swal.fire({
      title: 'Choose a user to revocate:',
      input: 'select',
      inputOptions: inputOptions,
      showCancelButton: true,
      showCloseButton: true,
      focusConfirm: false,
      confirmButtonText: 'Revocate',
    }).then(async (result) => {
      if (result.isConfirmed) {
        const selectedIndex = result.value;
        if (selectedIndex != null) {
          const selectedUsername = usernames[selectedIndex];

          const formData = new FormData();
          formData.append('username', selectedUsername);

          const response = await fetch('/offline_revo/', {
            method: 'POST',
            body: formData,
          });

          const data = await response.json();

          if (data.error == '0') {
            Swal.fire(
              'Revocated!',
              `User ${selectedUsername}'s authorization has been revocated.`,
              'success'
            );
          } else {
            Swal.fire(
              'Revocation Failed!',
              'Failed to revocate.',
              'error'
            );
          }
        }
      }
    });
  }
});