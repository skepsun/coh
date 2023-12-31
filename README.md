# Chain of hindsight

## Step1. 生成数据

```shell
# from origin: https://github.com/lhao499/chain-of-hindsight/tree/main
python hf_pack.py
```

## Step2. 简化数据

```shell
python simplify.py news_train_p,n,pn,np,aux.jsonl news_coh.jsonl 
```

## Step3. 放入现有框架进行训练

简化的数据格式适合使用LLaMA-Efficient-Tuning进行微调。应当是标准的（多轮）对话sft+预训练loss。

需要框架支持带有预训练loss的sft，我认为有两种做法：

1. 在LLaMA-Efficient-Tuning中则需要修改sft/workflow.py，但是trainer由于是继承的hf trainer，需要进一步修改 `compute_loss`或者 `training_step`。
2. 直接与预训练数据集混用，并在 `data/dataset_info.json` 把预训练数据中的   `text `放到sft模式下需要预测的 `response`里。

## Step4. 验证

根据你的基座模型的prompt template，在prompt后面加上正向引导的marker，比如：

```python
# baichuan
marker = "Generate a better article: "
prompt = "<reserved_102>{instruction}\n{marker}<reserved_103>"
```

如果依然用LLaMA-Efficient-Tuning进行预测，需要增加相应的template。

## thoughts

可能因为作者需要用TPU，所以他的实现是基于Jax的，很不方便；

数据预处理代码也极其繁琐，不过这也和他设计的prompt格式过于复杂有关;

生成的数据也是原来的几十倍大小，训练起来不见得有多快。

训练数据的质量很重要，最好是和sft模型同一来源的
