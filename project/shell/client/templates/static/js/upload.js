// 需要优化的的地方搜索 “优化”即可

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

              const response = await fetch('/online_auth/', {
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

  //删除按钮,点击后弹出是否确认删除
  const deleteButtons = document.querySelectorAll(".delete");

  deleteButtons.forEach(button => {
    button.addEventListener("click", () => {
      // 获取该文件元素
      const fileItem = button.closest(".file-item");

      Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then(async (result) => {
        if (result.isConfirmed) {
          const filename = fileItem.querySelector(".file-link").textContent;

          // 向后端发送选中的用户名和文件名
          const formData = new FormData();
          formData.append('documents', filename);

          const response = await fetch('/delete/', {
            method: 'POST',
            body: formData,
          });

          const data = await response.json();

          if (data.error == '0') {
            fileItem.parentNode.removeChild(fileItem);
            Swal.fire(
              'Deleted!',
              'Your file has been deleted.',
              'success'
            )
          } else {
            Swal.fire(
              'Delete Failed!',
              'Fail to delete this file.',
              'error'
            )
          }
        }
      })
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

// 以上分割线///////////////////////////////////////////////////////////////////////////////////////////////////////

// 根据文件名获取文件后缀，后续调用根据后缀来修改文件的图片显示
document.addEventListener("DOMContentLoaded", function () {
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
    case "md":
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

  Swal.fire({
    title: '新建文件',
    text: '请输入文件名称：',
    input: 'text',
    inputPlaceholder: '文件名称',
    showCancelButton: true,
    confirmButtonText: '创建',
    cancelButtonText: '取消',
  }).then((result) => {
    if (result.isConfirmed) {
      const fileName = result.value; // 获取用户输入的文件夹名称

      if (fileName) { // 如果用户输入了名称
        const newFolder = document.createElement('li');
        newFolder.className = 'file-item';

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

        //上传文件后要求用户输入对应的关键词
        Swal.fire({
          title: '<span class="swal2-title">Please Enter the <span class="keyword">KeyWord</span></span>',
          html: `<input id="swal-input1" class="swal2-input" placeholder="Keyword1">
             <input id="swal-input2" class="swal2-input" placeholder="Keyword2">
             <input id="swal-input3" class="swal2-input" placeholder="Keyword3">`,
          focusConfirm: false,
          showCancelButton: true, // 添加取消按钮
          confirmButtonText: '   OK',
          cancelButtonText: 'Cancel',
          preConfirm: () => {
            const key1 = Swal.getPopup().querySelector('#swal-input1').value
            const key2 = Swal.getPopup().querySelector('#swal-input2').value
            const key3 = Swal.getPopup().querySelector('#swal-input3').value
            if (!key1 && !key2 && !key3) {
              Swal.showValidationMessage(`Please enter all keywords!`)
            }
            return { fileName: fileName, key1: key1, key2: key2, key3: key3 }
          }
        }).then((result) => {
          if (result.isConfirmed) {
            const { fileName, key1, key2, key3 } = result.value;
            const kws = [key1, key2, key3];
            const documents = { [fileName]: kws };

            async function snedData() {
              //应该是可以在这里进行对应的后端传输
              const formData = new FormData();
              formData.append('documents', JSON.stringify(documents));

              try {
                // 使用 fetch API 发送数据
                const response = await fetch('/add/', {
                  method: 'POST',
                  body: formData,
                });
                const data = await response.json();

                if (data['error'] == '1') {
                  // 如果服务器返回了一个错误，你可以在这里处理它
                  const message = data['msg'];
                  errorMessageElement.innerText = message;
                  return false;
                } else {
                  Swal.fire({
                    icon: 'success',
                    title: 'Uploaded successfully!',
                  })
                }
              } catch (error) {
                console.error("error when sending data: ", error);
              }
            }

            snedData();
          }
        })

        fileList.appendChild(newFolder); // 将文件夹添加到file-list中
      }

      // 实现新建文件的按钮功能
      // 获取所有删除按钮
      FileButtonFunctions();

    }
  }
  )

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


    const lastName = getFileType(fileName);

    if (lastName == "word") {
      fileIconImg.className = "fas fa-file-word";
    }
    else if (lastName == "pdf") {
      fileIconImg.className = "fas fa-file-pdf";
    }
    else if (lastName == "txt") {
      fileIconImg.className = "fas fa-file-alt";
    }
    else if (lastName == "mp3") {
      fileIconImg.className = "fas fa-file-audio";
    }
    else if (lastName == "mp4") {
      fileIconImg.className = "fas fa-file-video";
    }
    else if (lastName == "image") {
      fileIconImg.className = "fas fa-file-image";
    }
    else if (lastName == "archive") {
      fileIconImg.className = "fas fa-file-archive";
    }
    else if (lastName == "exe") {
      fileIconImg.className = "fas fa-file-code";
    }
    else if (lastName == "aaa") {
      fileIconImg.className = "fas fa-file-alt";
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

    // // 添加收藏按钮
    // const favoriteBtn = document.createElement("button");
    // favoriteBtn.className = "favorite file-action";
    // favoriteBtn.id = 'new-btn';
    // const favoriteIcon = document.createElement("i");
    // favoriteIcon.className = "fas fa-star";
    // favoriteBtn.appendChild(favoriteIcon);
    // newFileItem.appendChild(favoriteBtn);

    document.getElementById("files").appendChild(newFileItem);
  }
  //给按钮添加功能
  FileButtonFunctions();

  //上传文件后要求用户输入对应的关键词
  Swal.fire({
    title: '<span class="swal2-title">Please Enter the <span class="keyword">KeyWord</span></span>',
    html: `<input id="swal-input1" class="swal2-input" placeholder="Keyword1">
             <input id="swal-input2" class="swal2-input" placeholder="Keyword2">
             <input id="swal-input3" class="swal2-input" placeholder="Keyword3">`,
    focusConfirm: false,
    showCancelButton: true, // 添加取消按钮
    confirmButtonText: '   OK',
    cancelButtonText: 'Cancel',
    preConfirm: () => {
      const key1 = Swal.getPopup().querySelector('#swal-input1').value
      const key2 = Swal.getPopup().querySelector('#swal-input2').value
      const key3 = Swal.getPopup().querySelector('#swal-input3').value
      if (!key1 && !key2 && !key3) {
        Swal.showValidationMessage(`Please enter all keywords!`)
      }
      return { key1: key1, key2: key2, key3: key3 }
    }
  }).then((result) => {
    if (result.isConfirmed) {
      const { key1, key2, key3 } = result.value;

      async function snedData() {
        //应该是可以在这里进行对应的后端传输
        const documents = { fileName: [key1, key2, key3] };
        const formData = new FormData();
        formData.append('documents', documents);
        try {
          // 使用 fetch API 发送数据
          const response = await fetch('/register_login/', {
            method: 'POST',
            body: formData,
          });
          const data = await response.json();

          if (data['error'] == '1') {
            // 如果服务器返回了一个错误，你可以在这里处理它
            const message = data['msg'];
            errorMessageElement.innerText = message;
            return false;
          } else {
            Swal.fire({
              icon: 'success',
              title: 'Uploaded successfully!',
            })
          }
        } catch (error) {
          console.error("error when sending data: ", error);
        }
      }

      snedData();
    }
  })


});






//排序按键，只实现了字母升序和字母降序
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

document.getElementById('searchButton').addEventListener('click', function (e) {
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
      window.location.href = '../search';
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