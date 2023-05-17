
const singUpBtn = document.querySelector('#sign-up-btn')
const singInBtn = document.querySelector('#sign-in-btn')
const container = document.querySelector('.container')

singUpBtn.addEventListener('click', () => {
  container.classList.add('sign-up-mode')
})
singInBtn.addEventListener('click', () => {
  container.classList.remove('sign-up-mode')
})



//哈希函数
async function hash(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
  return hashHex;
}

//登录:密码进行哈希
async function hashPassword(event) {
  event.preventDefault();

  // 获取输入字段的值
  const username = document.getElementById("username_login").value;
  const passwordInput = document.getElementById('password_login').value;
  const errorMessageElement = document.getElementById("error-message-login");


  // 在前端进行密码哈希操作
  const hashedPassword = await hash(passwordInput);
  // console.log(hashedPassword);

  // 将哈希后的密码设置到隐藏字段中
  // const hashedPasswordInput = document.getElementById('hashed_password');
  // hashedPasswordInput.value = hashedPassword;

  // 创建一个新的 FormData 实例
  const formData = new FormData();
  formData.append('type', '1')
  formData.append('username', username);
  formData.append('password', hashedPassword);

  // 使用 fetch API 发送数据
  const response = await fetch('/register_login/', {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();

  if (data['error']== '1') {
    // 如果服务器返回了一个错误，你可以在这里处理它
    const message = data['msg'];
    errorMessageElement.innerText = message;
    return false;
  }
  
  if (data['redirect']) {
    window.location.href = data['redirect'];
  }
}

//注册
//注册执行函数：密码输入错误返回值,并且将输入的密码进行哈希
async function validateForm(event) {
  event.preventDefault();

  const username = document.getElementById("username_regis").value;
  const password1 = document.getElementById("password_first").value;
  const password2 = document.getElementById("password_confirm").value;
  const errorMessageElement = document.getElementById("error-message-register");

  if (password1 !== password2) {
    errorMessageElement.innerText = "密码错误，请重新输入";
    return false;
  } else if (password1.length < 8) {
    errorMessageElement.innerText = "密码少于八位，请重新输入";
    return false;
  } else {
    errorMessageElement.innerText = "";

    // 对密码进行哈希处理
    const hashedPassword = await hash(password1);
    console.log("哈希后的密码: ", hashedPassword);

    // 创建一个新的 FormData 实例
    const formData = new FormData();
    formData.append('type', '0')
    formData.append('username', username);
    formData.append('password', hashedPassword);

    // 使用 fetch API 发送数据
    const response = await fetch('/register_login/', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (data['error']== '1') {
      // 如果服务器返回了一个错误，你可以在这里处理它
      const message = data['msg'];
      errorMessageElement.innerText = message;
      return false;
    }
    
    if (data['redirect']) {
      window.location.href = data['redirect'];
    }
  }
}


