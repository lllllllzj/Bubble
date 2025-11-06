import tkinter as tk
import random


class FloatBubbleText:
    def __init__(self, root):
        self.root = root
        self.root.title("一份神秘的礼物")
        self.root.attributes('-topmost', True)  # 置顶显示
        self.root.attributes('-alpha', 0.95)  # 透明度

        # 设置窗口大小为手机屏幕大小 (iPhone 14 Pro比例)
        window_width = 390
        window_height = 844
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - window_width) // 2
        y = (screen_h - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 设置窗口背景色为柔和的薰衣草色
        self.root.config(bg='#E8E5F5')

        self.window_width = window_width
        self.window_height = window_height

        # 可自定义:温暖关心的文案(大幅增加)
        self.text_list = [
            # 日常关心
            "记得多喝水哦~",
            "累了就休息一下吧",
            "辛苦了,要好好照顾自己",
            "天冷了,注意保暖",
            "今天吃什么好吃的?",
            "注意安全哦",
            "早点睡,别熬夜",
            "记得按时吃饭",
            "出门带伞哦",
            "路上小心",
            "别着凉了",
            "记得吃早餐",

            # 赞美鼓励
            "你的笑容最美",
            "你真的很棒!",
            "你值得所有美好",
            "你是最特别的",
            "你的眼睛会发光",
            "你已经很努力了",
            "你很优秀",
            "你很可爱",
            "你真温柔",
            "你真善良",

            # 情感表达
            "想你了...",
            "遇见你真好",
            "想抱抱你",
            "我会一直陪着你",
            "有我在呢",
            "想听你的声音",
            "想见你",
            "想和你在一起",
            "想牵你的手",
            "想给你一个拥抱",
            "永远支持你",
            "永远陪着你",

            # 温暖问候
            "晚安,做个好梦",
            "早安,美好的一天",
            "今天也要开心呀",
            "今天过得好吗?",
            "最近还好吗?",
            "周末快乐!",
            "新的一天,加油!",
            "今天也爱你",

            # 安慰支持
            "不开心的话就跟我说",
            "加油!我相信你",
            "慢慢来,不着急",
            "别担心,会好的",
            "一切都会好起来的",
            "我理解你",
            "你不是一个人",
            "有什么需要随时找我",
            "别给自己太大压力",
            "做你自己就好",

            # 生活细节
            "今天天气真好",
            "出去走走吧",
            "适当运动一下",
            "放松一下心情",
            "听听音乐吧",
            "看场电影吧",
            "好好休息",
            "该睡觉啦",

            # 甜蜜话语
            "你今天真好看",
            "超级想你",
            "想陪你看日落",
            "想陪你散步",
            "想给你做饭",
            "想和你分享今天",
            "每天都想见到你",
            "你是我的小太阳",
            "你让我很开心",
            "因为你,每天都很美好",
        ]

        # 创建可用文案列表(用于跟踪哪些文案还未使用)
        self.available_texts = self.text_list.copy()

        # 打乱顺序,让每次循环的顺序都不同
        random.shuffle(self.available_texts)

        # 可自定义:气泡背景颜色(类似微信的柔和配色)
        self.bubble_colors = [
            "#95EC69",  # 微信绿
            "#A8E6F5",  # 浅蓝
            "#FFE0B2",  # 浅橙
            "#F8BBD0",  # 粉色
            "#E1BEE7",  # 浅紫
            "#FFECB3",  # 浅黄
            "#C5E1A5",  # 浅绿
        ]
        self.bubbles = []  # 存储所有气泡

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=12, **kwargs):
        """在Canvas上绘制圆角矩形"""
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def ease_out_back(self, x):
        """回弹缓动函数"""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2)

    def animate_bubble_entry(self, canvas, shadow_canvas, target_x, target_y,
                             bubble_width, bubble_height, step=0):
        """快速丝滑的气泡弹出动画"""
        max_steps = 18  # 减少步数,加快动画速度

        if step <= max_steps:
            # 计算进度
            progress = step / max_steps

            # 使用回弹缓动函数
            eased = self.ease_out_back(progress)

            # 计算缩放 (从0.4到1.08再回到1.0)
            if progress < 0.75:
                current_scale = 0.4 + eased * 0.68
            else:
                # 最后阶段轻微回弹
                overshoot = (progress - 0.75) / 0.25
                current_scale = 1.08 - overshoot * 0.08

            # 计算Y轴位移 (轻微上浮效果)
            offset_y = int((1 - eased) * 15)

            # 更新位置
            canvas.place(x=target_x, y=target_y + offset_y)
            shadow_canvas.place(x=target_x + 2, y=target_y + offset_y + 2)

            # 继续动画,使用更短的间隔
            self.root.after(8, lambda: self.animate_bubble_entry(
                canvas, shadow_canvas, target_x, target_y,
                bubble_width, bubble_height, step + 1
            ))

    def create_bubble(self, delay=0):
        """创建单个气泡,支持延迟"""
        # 如果有延迟,则延迟执行
        if delay > 0:
            self.root.after(delay, lambda: self.create_bubble(0))
            return

        # 如果所有文案都已使用,重新填充并打乱顺序
        if not self.available_texts:
            self.available_texts = self.text_list.copy()
            random.shuffle(self.available_texts)  # 打乱顺序,每次循环都不同

        # 随机选择一个未使用的文案
        text = random.choice(self.available_texts)
        # 从可用列表中移除已使用的文案
        self.available_texts.remove(text)

        bg_color = random.choice(self.bubble_colors)
        font_size = random.randint(13, 16)  # 适配手机屏幕的字体大小

        # 预先计算气泡大小
        temp_label = tk.Label(self.root, text=text, font=("微软雅黑", font_size, "normal"))
        temp_label.update_idletasks()
        text_width = temp_label.winfo_reqwidth() + 24
        text_height = temp_label.winfo_reqheight() + 14
        bubble_width = max(text_width, 70)
        bubble_height = max(text_height, 32)
        temp_label.destroy()

        # 更均匀的位置分布 - 扩大范围,包括边缘位置
        # X轴:从10到窗口宽度-气泡宽度-10
        max_x = self.window_width - bubble_width - 10
        x = random.randint(10, max(10, max_x))

        # Y轴:从50到窗口高度-气泡高度-50,更均匀分布
        max_y = self.window_height - bubble_height - 50
        y = random.randint(50, max(50, max_y))

        # 创建阴影Canvas - 精确大小
        shadow_canvas = tk.Canvas(
            self.root,
            width=bubble_width,
            height=bubble_height,
            bg='#E8E5F5',
            highlightthickness=0
        )
        shadow_canvas.place(x=x + 2, y=y + 2)

        # 绘制阴影圆角矩形
        self.create_rounded_rectangle(
            shadow_canvas, 0, 0, bubble_width, bubble_height,
            radius=10, fill='#B8B8B8', outline=''
        )

        # 创建主气泡Canvas - 精确大小
        canvas = tk.Canvas(
            self.root,
            width=bubble_width,
            height=bubble_height,
            bg='#E8E5F5',
            highlightthickness=0
        )
        canvas.place(x=x, y=y)

        # 绘制圆角矩形背景
        self.create_rounded_rectangle(
            canvas, 0, 0, bubble_width, bubble_height,
            radius=10, fill=bg_color, outline=''
        )

        # 创建文字标签
        text_label = tk.Label(
            canvas,
            text=text,
            font=("微软雅黑", font_size, "normal"),
            fg='#333333',
            bg=bg_color,
            wraplength=bubble_width - 16,
            justify='center'
        )
        canvas.create_window(
            bubble_width // 2, bubble_height // 2,
            window=text_label, anchor='center'
        )

        # 启动快速弹出动画
        self.animate_bubble_entry(canvas, shadow_canvas, x, y, bubble_width, bubble_height)

        self.bubbles.append((canvas, shadow_canvas))

    def create_multiple_bubbles(self):
        """同时创建多个气泡"""
        # 随机生成2-4个气泡
        num_bubbles = random.randint(2, 4)

        for i in range(num_bubbles):
            # 每个气泡有小延迟,形成连续弹出效果
            delay = i * 50  # 50ms的间隔
            self.create_bubble(delay)

    def auto_create_bubbles(self):
        """自动创建气泡 - 持续循环"""
        # 均匀生成气泡组 - 固定时间间隔
        if random.random() < 0.8:  # 80%概率生成新气泡组
            self.create_multiple_bubbles()

        # 每500毫秒检查一次,持续循环
        self.root.after(500, self.auto_create_bubbles)


if __name__ == "__main__":
    root = tk.Tk()
    app = FloatBubbleText(root)
    app.auto_create_bubbles()  # 启动自动生成气泡
    root.mainloop()
