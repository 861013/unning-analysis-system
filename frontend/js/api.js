// API基础配置
const API_BASE_URL = 'http://localhost:8000';

// API请求封装
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${url}`, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

// 获取运动数据列表
async function getExerciseData(userId = null) {
    const url = userId ? `/api/exercise?userId=${userId}` : '/api/exercise';
    return await apiRequest(url);
}

// 创建运动数据
async function createExerciseData(data) {
    return await apiRequest('/api/exercise', 'POST', data);
}

// 获取统计数据
async function getStatistics(userId = null) {
    const url = userId ? `/api/statistics?userId=${userId}` : '/api/statistics';
    return await apiRequest(url);
}

// 导出CSV
async function exportCSV(userId = null) {
    const url = userId ? `/api/export/csv?userId=${userId}` : '/api/export/csv';
    const response = await fetch(`${API_BASE_URL}${url}`);
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = 'running_data.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
}

