// pages/login/login.js
const app = getApp()
const api = require('../../utils/api.js')

Page({
  data: {
    loginType: 'phone', // phone, email, wechat
    phone: '',
    email: '',
    password: '',
    showRegister: false,
    registerData: {
      username: '',
      phone: '',
      email: '',
      password: '',
      gender: '',
      birthday: ''
    }
  },

  onLoad() {
    // 检查是否已登录
    if (app.globalData.isLoggedIn) {
      wx.switchTab({
        url: '/pages/index/index'
      })
    }
  },

  // 切换登录方式
  switchLoginType(e) {
    this.setData({
      loginType: e.currentTarget.dataset.type
    })
  },

  // 切换注册/登录
  toggleRegister() {
    this.setData({
      showRegister: !this.data.showRegister
    })
  },

  // 手机号输入
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value })
  },

  // 邮箱输入
  onEmailInput(e) {
    this.setData({ email: e.detail.value })
  },

  // 密码输入
  onPasswordInput(e) {
    this.setData({ password: e.detail.value })
  },

  // 登录
  async handleLogin() {
    const { loginType, phone, email, password } = this.data

    if (loginType === 'phone' && !phone) {
      wx.showToast({ title: '请输入手机号', icon: 'none' })
      return
    }

    if (loginType === 'email' && !email) {
      wx.showToast({ title: '请输入邮箱', icon: 'none' })
      return
    }

    if (!password && loginType !== 'wechat') {
      wx.showToast({ title: '请输入密码', icon: 'none' })
      return
    }

    wx.showLoading({ title: '登录中...' })

    try {
      const loginData = {}
      if (loginType === 'phone') {
        loginData.phone = phone
      } else if (loginType === 'email') {
        loginData.email = email
      } else if (loginType === 'wechat') {
        // 微信登录需要先获取code
        const res = await wx.login()
        loginData.wechat_openid = res.code // 实际应该通过code换取openid
      }
      loginData.password = password

      const result = await api.auth.login(loginData)
      
      // 保存token
      app.setLoginStatus(true, result.access_token)
      
      wx.hideLoading()
      wx.showToast({ title: '登录成功', icon: 'success' })
      
      // 跳转到首页
      setTimeout(() => {
        wx.switchTab({
          url: '/pages/index/index'
        })
      }, 1500)
    } catch (err) {
      wx.hideLoading()
      wx.showToast({
        title: err.message || '登录失败',
        icon: 'error'
      })
    }
  },

  // 注册
  async handleRegister() {
    const { registerData } = this.data

    if (!registerData.phone && !registerData.email) {
      wx.showToast({ title: '请输入手机号或邮箱', icon: 'none' })
      return
    }

    if (!registerData.password || registerData.password.length < 6) {
      wx.showToast({ title: '密码至少6位', icon: 'none' })
      return
    }

    wx.showLoading({ title: '注册中...' })

    try {
      await api.auth.register(registerData)
      
      wx.hideLoading()
      wx.showToast({ title: '注册成功', icon: 'success' })
      
      // 自动登录
      setTimeout(() => {
        this.handleLogin()
      }, 1500)
    } catch (err) {
      wx.hideLoading()
      wx.showToast({
        title: err.message || '注册失败',
        icon: 'error'
      })
    }
  }
})

