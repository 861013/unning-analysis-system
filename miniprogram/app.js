// app.js
App({
  onLaunch() {
    // 小程序启动时初始化
    console.log('跑步分析系统小程序启动')
    
    // 检查登录状态
    const token = wx.getStorageSync('token')
    if (token) {
      this.globalData.isLoggedIn = true
    }
  },
  
  globalData: {
    apiBaseUrl: 'http://localhost:8000', // 后端API地址，生产环境需要配置HTTPS域名
    userInfo: null,
    isLoggedIn: false,
    token: null
  },
  
  // 设置用户信息
  setUserInfo(userInfo) {
    this.globalData.userInfo = userInfo
  },
  
  // 设置登录状态
  setLoginStatus(isLoggedIn, token) {
    this.globalData.isLoggedIn = isLoggedIn
    this.globalData.token = token
    if (token) {
      wx.setStorageSync('token', token)
    } else {
      wx.removeStorageSync('token')
    }
  }
})

