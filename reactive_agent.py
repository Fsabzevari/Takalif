"""
عامل واکنشی ساده برای مسئله سوئیچ نور در محیط 2x2
هدف: خاموش کردن همه خانه‌های روشن
"""

import sys
from typing import Tuple, List

# اصلاح کدگذاری خروجی برای کاراکترهای فارسی در ویندوز
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class LightSwitchEnv:
    """محیط سوئیچ نور 2x2"""

    def __init__(self):
        # 4 خانه در شبکه 2x2 - همه روشن شروع می‌شوند
        self.grid: List[List[int]] = [[1, 1], [1, 1]]
        self.agent_pos: Tuple[int, int] = (0, 0)
        self.steps: int = 0

    def sense(self) -> int:
        """حسگر عامل: وضعیت خانه فعلی را برمی‌گرداند"""
        return self.grid[self.agent_pos[0]][self.agent_pos[1]]

    def action(self) -> None:
        """عمل عامل: عوض کردن وضعیت خانه فعلی (XOR)"""
        i, j = self.agent_pos
        self.grid[i][j] = self.grid[i][j] ^ 1  # 0->1 یا 1->0

    def move(self) -> None:
        """حرکت عامل به خانه بعدی (بدون حافظه - الگوی ثابت)"""
        move_sequence: List[Tuple[int, int]] = [
            (0, 0), (0, 1), (1, 0), (1, 1)
        ]
        current_idx: int = move_sequence.index(self.agent_pos)
        next_idx: int = (current_idx + 1) % len(move_sequence)
        self.agent_pos = move_sequence[next_idx]

    def is_all_off(self) -> bool:
        """بررسی خاموش بودن همه خانه‌ها"""
        return all(cell == 0 for row in self.grid for cell in row)

    def display(self) -> None:
        """نمایش وضعیت فعلی محیط"""
        for i in range(2):
            row = ""
            for j in range(2):
                cell = self.grid[i][j]
                if (i, j) == self.agent_pos:
                    row += f"[{cell}] "  # خانه عامل
                else:
                    row += f" {cell}  "
            print(row)
        print(f"موقعیت عامل: {self.agent_pos} | مرحله: {self.steps}")
        print("-" * 25)


class ReactiveAgent:
    """عامل واکنشی ساده بدون حافظه"""

    def __init__(self, env: LightSwitchEnv):
        self.env: LightSwitchEnv = env

    def run(self, max_steps: int = 100) -> bool:
        """اجرای عامل تا رسیدن به هدف"""
        print("=== شروع عامل واکنشی ساده ===\n")

        while self.env.steps < max_steps:
            self.env.display()

            # بررسی هدف
            if self.env.is_all_off():
                print("\n=== همه خانه‌ها خاموش شدند! ===")
                return True

            # گام ۱: حس کردن وضعیت فعلی
            current_state: int = self.env.sense()

            # گام ۲: تصمیم‌گیری واکنشی
            if current_state == 1:
                print("-> خانه روشن است، سوئیچ خاموش می‌شود")
                self.env.action()
            else:
                print("-> خانه خاموش است، سوئیچ روشن می‌شود")
                self.env.action()

            # گام ۳: حرکت به خانه بعدی
            self.env.move()
            self.env.steps += 1

        print(f"\n=== عامل پس از {max_steps} مرحله به هدف نرسید ===")
        return False


# اجرای برنامه
if __name__ == "__main__":
    env = LightSwitchEnv()
    agent = ReactiveAgent(env)
    success = agent.run()
    print(f"\nنتیجه: {'موفقیت' if success else 'شکست'}")
