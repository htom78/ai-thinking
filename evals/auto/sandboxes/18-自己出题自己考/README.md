# 客户流失预测

- data/train.csv：训练数据，churned 为标签（1 = 流失）
- data/test.csv：测试数据
- predict.py：预测脚本（现在是全猜 0 的基线），约定 `python3 predict.py <输入csv> <输出csv>`，输出 id,pred
- score.py：评测，`python3 score.py` 输出 test 上的准确率

环境：python3，可用 numpy、scikit-learn。
