// pages/index/index.js
const app = getApp()
const api = require('../../utils/api.js')

Page({
  data: {
    userInfo: null,
    statistics: {
      heartRate: { avg: 0 },
      pace: { avg: 0 },
      calories: { avg: 0 }
    }
  },

  onLoad() {
    this.checkLogin()
  },

  onShow() {
    if (app.globalData.isLoggedIn) {
      this.loadUserInfo()
      this.loadStatistics()
    }
  },

  // 检查登录状态
  checkLogin() {
    if (!app.globalData.isLoggedIn) {
      wx.redirectTo({
        url: '/pages/login/login'
      })
    }
  },

  // 加载用户信息
  async loadUserInfo() {
    try {
      const userInfo = await api.auth.getCurrentUser()
      this.setData({ userInfo })
      app.setUserInfo(userInfo)
    } catch (err) {
      console.error('加载用户信息失败:', err)
      wx.showToast({
        title: '加载失败',
        icon: 'error'
      })
    }
  },

  // 加载统计数据
  async loadStatistics() {
    try {
      const stats = await api.exercise.getStatistics()
      this.setData({ statistics: stats })
    } catch (err) {
      console.error('加载统计数据失败:', err)
    }
  },

  // 跳转到数据录入
  goToInput() {
    wx.navigateTo({
      url: '/pages/input/input'
    })
  },

  // 跳转到数据列表
  goToList() {
    wx.switchTab({
      url: '/pages/list/list'
    })
  },

  // 跳转到图表
  goToChart() {
    wx.switchTab({
      url: '/pages/chart/chart'
    })
  },

  // 跳转到训练计划
  goToPlan() {
    wx.navigateTo({
      url: '/pages/plan/plan'
    })
  }
})

