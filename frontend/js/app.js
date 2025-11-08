// 全局变量
let heartRateChart = null;
let paceChart = null;
let caloriesChart = null;

// 标签页切换
function showTab(tabName) {
    // 隐藏所有标签页
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 移除所有按钮的active类
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示选中的标签页
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // 激活对应的按钮
    event.target.classList.add('active');
    
    // 如果是图表标签页，加载图表数据
    if (tabName === 'chart') {
        loadChartData();
    }
}

// 显示消息
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type} show`;
    messageDiv.textContent = message;
    
    const container = document.querySelector('.container');
    const header = document.querySelector('header');
    header.insertAdjacentElement('afterend', messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// 提交表单
document.getElementById('exercise-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        userId: document.getElementById('userId').value,
        basicInfo: {
            gender: document.getElementById('gender').value || undefined,
            age: document.getElementById('age').value ? parseInt(document.getElementById('age').value) : undefined,
            height: document.getElementById('height').value ? parseFloat(document.getElementById('height').value) : undefined,
            weight: document.getElementById('weight').value ? parseFloat(document.getElementById('weight').value) : undefined,
            bodyFat: document.getElementById('bodyFat').value ? parseFloat(document.getElementById('bodyFat').value) : undefined
        },
        bandData: {
            heartRate: document.getElementById('heartRate').value ? parseInt(document.getElementById('heartRate').value) : undefined,
            pace: document.getElementById('pace').value ? parseFloat(document.getElementById('pace').value) : undefined,
            calories: document.getElementById('calories').value ? parseInt(document.getElementById('calories').value) : undefined,
            trainingLoad: document.getElementById('trainingLoad').value ? parseInt(document.getElementById('trainingLoad').value) : undefined,
            sleep: document.getElementById('sleepDuration').value ? {
                duration: parseFloat(document.getElementById('sleepDuration').value)
            } : undefined
        },
        treadmillData: {
            speed: document.getElementById('speed').value ? parseFloat(document.getElementById('speed').value) : undefined,
            incline: document.getElementById('incline').value ? parseFloat(document.getElementById('incline').value) : undefined,
            duration: document.getElementById('duration').value ? parseInt(document.getElementById('duration').value) : undefined,
            distance: document.getElementById('distance').value ? parseFloat(document.getElementById('distance').value) : undefined
        }
    };
    
    // 移除undefined字段
    Object.keys(formData.basicInfo).forEach(key => {
        if (formData.basicInfo[key] === undefined) delete formData.basicInfo[key];
    });
    Object.keys(formData.bandData).forEach(key => {
        if (formData.bandData[key] === undefined) delete formData.bandData[key];
    });
    Object.keys(formData.treadmillData).forEach(key => {
        if (formData.treadmillData[key] === undefined) delete formData.treadmillData[key];
    });
    
    try {
        await createExerciseData(formData);
        showMessage('数据提交成功！', 'success');
        document.getElementById('exercise-form').reset();
        document.getElementById('userId').value = 'user001';
    } catch (error) {
        showMessage('数据提交失败: ' + error.message, 'error');
    }
});

// 加载运动数据列表
async function loadExerciseData() {
    const userId = document.getElementById('filter-userId').value;
    const listDiv = document.getElementById('exercise-list');
    listDiv.innerHTML = '<p>加载中...</p>';
    
    try {
        const data = await getExerciseData(userId || null);
        
        if (data.length === 0) {
            listDiv.innerHTML = '<p>暂无数据</p>';
            return;
        }
        
        listDiv.innerHTML = data.map(item => {
            const date = new Date(item.timestamp).toLocaleString('zh-CN');
            const bandData = item.bandData || {};
            const treadmillData = item.treadmillData || {};
            const basicInfo = item.basicInfo || {};
            
            return `
                <div class="data-item">
                    <div class="data-item-header">
                        <span class="data-item-date">${date}</span>
                        <span class="data-item-user">用户: ${item.userId}</span>
                    </div>
                    <div class="data-item-content">
                        ${bandData.heartRate ? `
                            <div class="data-item-field">
                                <label>心率</label>
                                <span>${bandData.heartRate} bpm</span>
                            </div>
                        ` : ''}
                        ${bandData.pace ? `
                            <div class="data-item-field">
                                <label>配速</label>
                                <span>${bandData.pace} min/km</span>
                            </div>
                        ` : ''}
                        ${bandData.calories ? `
                            <div class="data-item-field">
                                <label>卡路里</label>
                                <span>${bandData.calories} kcal</span>
                            </div>
                        ` : ''}
                        ${treadmillData.speed ? `
                            <div class="data-item-field">
                                <label>速度</label>
                                <span>${treadmillData.speed} km/h</span>
                            </div>
                        ` : ''}
                        ${treadmillData.distance ? `
                            <div class="data-item-field">
                                <label>距离</label>
                                <span>${treadmillData.distance} km</span>
                            </div>
                        ` : ''}
                        ${basicInfo.weight ? `
                            <div class="data-item-field">
                                <label>体重</label>
                                <span>${basicInfo.weight} kg</span>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        listDiv.innerHTML = `<p style="color: red;">加载失败: ${error.message}</p>`;
    }
}

// 加载图表数据
async function loadChartData() {
    try {
        const stats = await getStatistics();
        
        // 更新统计数据
        const statsDiv = document.getElementById('statistics-info');
        statsDiv.innerHTML = `
            <div class="stat-item">
                <label>心率平均值</label>
                <div class="value">${stats.heartRate.avg} bpm</div>
            </div>
            <div class="stat-item">
                <label>心率最大值</label>
                <div class="value">${stats.heartRate.max} bpm</div>
            </div>
            <div class="stat-item">
                <label>心率最小值</label>
                <div class="value">${stats.heartRate.min} bpm</div>
            </div>
            <div class="stat-item">
                <label>配速平均值</label>
                <div class="value">${stats.pace.avg} min/km</div>
            </div>
            <div class="stat-item">
                <label>卡路里平均值</label>
                <div class="value">${stats.calories.avg} kcal</div>
            </div>
        `;
        
        // 绘制心率图表
        const heartRateCtx = document.getElementById('heartRateChart').getContext('2d');
        if (heartRateChart) {
            heartRateChart.destroy();
        }
        heartRateChart = new Chart(heartRateCtx, {
            type: 'line',
            data: {
                labels: stats.dates.slice(0, stats.heartRate.data.length),
                datasets: [{
                    label: '心率 (bpm)',
                    data: stats.heartRate.data,
                    borderColor: 'rgb(102, 126, 234)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '心率趋势图'
                    }
                }
            }
        });
        
        // 绘制配速图表
        const paceCtx = document.getElementById('paceChart').getContext('2d');
        if (paceChart) {
            paceChart.destroy();
        }
        paceChart = new Chart(paceCtx, {
            type: 'line',
            data: {
                labels: stats.dates.slice(0, stats.pace.data.length),
                datasets: [{
                    label: '配速 (min/km)',
                    data: stats.pace.data,
                    borderColor: 'rgb(118, 75, 162)',
                    backgroundColor: 'rgba(118, 75, 162, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '配速趋势图'
                    }
                }
            }
        });
        
        // 绘制卡路里图表
        const caloriesCtx = document.getElementById('caloriesChart').getContext('2d');
        if (caloriesChart) {
            caloriesChart.destroy();
        }
        caloriesChart = new Chart(caloriesCtx, {
            type: 'bar',
            data: {
                labels: stats.dates.slice(0, stats.calories.data.length),
                datasets: [{
                    label: '卡路里 (kcal)',
                    data: stats.calories.data,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgb(102, 126, 234)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '卡路里消耗柱状图'
                    }
                }
            }
        });
    } catch (error) {
        console.error('加载图表数据失败:', error);
        showMessage('加载图表数据失败: ' + error.message, 'error');
    }
}

// 导出CSV（前端函数）
async function exportCSVData() {
    try {
        const userId = document.getElementById('filter-userId')?.value || null;
        await exportCSV(userId);
        showMessage('CSV导出成功！', 'success');
    } catch (error) {
        showMessage('CSV导出失败: ' + error.message, 'error');
    }
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    loadExerciseData();
});

