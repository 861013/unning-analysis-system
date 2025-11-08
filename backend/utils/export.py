from fastapi.responses import StreamingResponse, Response
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import csv
import io
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体（需要字体文件，这里使用默认字体）
# pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.ttf'))


async def export_to_csv(data: List[dict], filename: str = "data.csv") -> StreamingResponse:
    """导出数据为CSV格式"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    if not data:
        writer.writerow(["暂无数据"])
    else:
        # 写入表头
        headers = list(data[0].keys())
        writer.writerow(headers)
        
        # 写入数据
        for row in data:
            writer.writerow([row.get(header, "") for header in headers])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


async def export_to_json(data: List[dict], filename: str = "data.json") -> Response:
    """导出数据为JSON格式"""
    json_data = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    
    return Response(
        content=json_data,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


async def export_to_pdf(data: List[dict], title: str = "数据导出", filename: str = "data.pdf") -> StreamingResponse:
    """导出数据为PDF格式"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # 样式
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#333333'),
        spaceAfter=30,
        alignment=1  # 居中
    )
    
    # 标题
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    if not data:
        story.append(Paragraph("暂无数据", styles['Normal']))
    else:
        # 准备表格数据
        headers = list(data[0].keys())
        table_data = [headers]
        
        for row in data:
            table_data.append([str(row.get(header, "")) for header in headers])
        
        # 创建表格
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        story.append(table)
    
    # 生成PDF
    doc.build(story)
    buffer.seek(0)
    
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


async def export_training_plan_to_pdf(plan_data: dict, filename: str = "training_plan.pdf") -> StreamingResponse:
    """导出训练计划为PDF格式"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # 样式
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#333333'),
        spaceAfter=30,
        alignment=1
    )
    
    # 标题
    title = plan_data.get("title", "训练计划")
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # 计划信息
    if plan_data.get("duration"):
        story.append(Paragraph(f"计划时长：{plan_data['duration']}周", styles['Normal']))
    if plan_data.get("goal"):
        story.append(Paragraph(f"训练目标：{plan_data['goal']}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    
    # 每周训练安排
    if plan_data.get("weekly_schedule"):
        story.append(Paragraph("每周训练安排", styles['Heading2']))
        for week in plan_data["weekly_schedule"]:
            week_text = f"第{week.get('week', '')}周：训练日 {', '.join(week.get('training_days', []))}，休息日 {', '.join(week.get('rest_days', []))}"
            story.append(Paragraph(week_text, styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))
    
    # 每日训练计划
    if plan_data.get("daily_plans"):
        story.append(Paragraph("每日训练计划", styles['Heading2']))
        for day_plan in plan_data["daily_plans"]:
            day_text = f"{day_plan.get('day', '')}：热身 {day_plan.get('warmup', '')}，主训练 {day_plan.get('main', '')}，放松 {day_plan.get('cooldown', '')}"
            story.append(Paragraph(day_text, styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))
    
    # 训练建议
    if plan_data.get("suggestions"):
        story.append(Paragraph("训练建议", styles['Heading2']))
        for suggestion in plan_data["suggestions"]:
            story.append(Paragraph(f"• {suggestion}", styles['Normal']))
    
    # 生成PDF
    doc.build(story)
    buffer.seek(0)
    
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

