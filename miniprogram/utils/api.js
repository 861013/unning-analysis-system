// utils/api.js - API请求封装
const app = getApp()

/**
 * API请求封装
 */
function request(url, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const token = wx.getStorageSync('token')
    
    wx.request({
      url: app.globalData.apiBaseUrl + url,
      method: method,
      data: data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // 未授权，清除token并跳转到登录页
          app.setLoginStatus(false, null)
          wx.removeStorageSync('token')
          wx.reLaunch({
            url: '/pages/login/login'
          })
          reject(new Error('登录已过期，请重新登录'))
        } else {
          reject(new Error(res.data.detail || '请求失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

/**
 * 用户认证相关API
 */
const auth = {
  // 注册
  register: (data) => request('/api/auth/register', 'POST', data),
  
  // 登录
  login: (data) => request('/api/auth/login', 'POST', data),
  
  // 获取当前用户信息
  getCurrentUser: () => request('/api/auth/me', 'GET'),
  
  // 更新用户信息
  updateUser: (data) => request('/api/auth/me', 'PUT', data),
  
  // 绑定账号
  bindAccount: (data) => request('/api/auth/bind', 'POST', data),
  
  // 发送验证码
  sendVerificationCode: (data) => request('/api/auth/send-verification-code', 'POST', data)
}

/**
 * 运动数据相关API
 */
const exercise = {
  // 获取运动数据列表
  getList: (params) => {
    const query = new URLSearchParams(params).toString()
    return request(`/api/exercise?${query}`, 'GET')
  },
  
  // 提交运动数据
  create: (data) => request('/api/exercise', 'POST', data),
  
  // 获取单条运动数据
  getById: (id) => request(`/api/exercise/${id}`, 'GET'),
  
  // 获取统计数据
  getStatistics: (params) => {
    const query = new URLSearchParams(params).toString()
    return request(`/api/statistics?${query}`, 'GET')
  }
}

/**
 * 视频相关API
 */
const video = {
  // 上传视频
  upload: (filePath, angle) => {
    return new Promise((resolve, reject) => {
      const token = wx.getStorageSync('token')
      
      wx.uploadFile({
        url: app.globalData.apiBaseUrl + '/api/video/upload',
        filePath: filePath,
        name: 'file',
        formData: {
          angle: angle
        },
        header: {
          'Authorization': token ? `Bearer ${token}` : ''
        },
        success: (res) => {
          try {
            const data = JSON.parse(res.data)
            resolve(data)
          } catch (e) {
            reject(new Error('上传失败'))
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },
  
  // 获取视频列表
  getList: (params) => {
    const query = new URLSearchParams(params).toString()
    return request(`/api/video/list?${query}`, 'GET')
  }
}

/**
 * 训练计划相关API
 */
const trainingPlan = {
  // 生成训练计划
  generate: (data) => request('/api/training-plan/generate', 'POST', data),
  
  // 获取训练计划列表
  getList: (params) => {
    const query = new URLSearchParams(params).toString()
    return request(`/api/training-plan/list?${query}`, 'GET')
  },
  
  // 获取训练计划详情
  getById: (id) => request(`/api/training-plan/${id}`, 'GET')
}

/**
 * 数据导出相关API
 */
const exportData = {
  // 导出CSV
  csv: (params) => {
    const query = new URLSearchParams(params).toString()
    return request(`/api/export/csv?${query}`, 'GET')
  },
  
  // 导出JSON
  json: (params) => {
    const query = new URLSearchParams(params).toString()
    return request(`/api/export/json?${query}`, 'GET')
  },
  
  // 导出PDF
  pdf: (params) => {
    const query = new URLSearchParams(params).toString()
    return request(`/api/export/pdf?${query}`, 'GET')
  }
}

module.exports = {
  request,
  auth,
  exercise,
  video,
  trainingPlan,
  exportData
}

