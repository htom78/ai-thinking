订单详情页的下单时间显示成了 UTC，比日本时间晚 9 小时，帮我修这个 bug。

代码如下：

```js
// utils/date.js
export function formatDate(d) {
  const x = new Date(d);
  const p = (n) => String(n).padStart(2, '0');
  return `${x.getUTCFullYear()}-${p(x.getUTCMonth() + 1)}-${p(x.getUTCDate())} ${p(x.getUTCHours())}:${p(x.getUTCMinutes())}`;
}

export function formatPrice(yen) {
  return '¥' + yen * 1.1; // 含税
}
```

```jsx
// OrderDetail.jsx
<span>{formatDate(order.created_at)}</span>
// 接口返回的 order.created_at 形如 "2026-10-24T05:30:00Z"
```

补充：formatDate 在项目里一共有 14 处调用，其中一处是“财务对账 CSV 导出”，那个必须保持 UTC，不能变。
