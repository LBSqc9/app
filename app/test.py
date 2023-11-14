from transformers import AutoConfig, AutoModel, AutoTokenizer
import torch
import os

tokenizer = AutoTokenizer.from_pretrained("D:\chatglm2-6b\model", trust_remote_code=True)

config = AutoConfig.from_pretrained("D:\chatglm2-6b\model", trust_remote_code=True, pre_seq_len=128)
model = AutoModel.from_pretrained("D:\chatglm2-6b\model", config=config, trust_remote_code=True)
prefix_state_dict = torch.load(os.path.join("D:\chatglm2-6b\src\ptuning\output\second-chatglm2-6b-pt-128-2e-2\checkpoint-3000", "pytorch_model.bin"))
print("stop 1")
new_prefix_state_dict = {}
for k, v in prefix_state_dict.items():
    if k.startswith("transformer.prefix_encoder."):
        new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
print("stop 2")
model = model.quantize(4)
model = model.half().cuda()
print("stop 3")
model.transformer.prefix_encoder.float()
model = model.eval()
print("stop 4")
response, history = model.chat(tokenizer, "经审理查明：被告徐萧玉曾与案外人周浩斌合伙经营DIY打印店，后周浩斌退伙。被告徐萧玉遂联系原告封雷合伙经营该打印店，并要求封雷向其支付结算给周浩斌的退伙费10665元。2021年3月22日，被告徐萧玉作为甲方，原告封雷作为乙方，签订《参股与协议书》，载明：“甲方现拥有DIY打印店100%的股份，甲方将自己40%的股份转让给乙方，甲乙两方按上述占有股权比例分配公司股利及承担义务。二、本协议一式两份，双方各执一份，具有同等法律效益”。次日，原告封雷向被告徐萧玉微信转账10665元。后该DIY打印店因故被所在学校收回，双方合伙未实际经营，原告封雷遂要求被告徐萧玉退还其支付的10665元。2021年10月21日，被告徐萧玉就上述10665元向原告封雷出具《欠条》一份，载明：“出款人：封雷，欠款人：徐萧玉，……出款人借款壹万零陆佰陆拾伍圆整（小写人民币：10665元），支付方式：微信支付、支付宝支付，还款计划：从2021年11月1日起至2022年6月30为止，每月还款壹仟伍佰圆整（小写人民币：1500元），还完为止”。以上事实，有原被告的陈述及原告提交的《欠条》、《参股与协议书》等证据予以证实，本院予以确认。", history=[])

with open('reason.txt', 'w', encoding='utf-8') as file:
    file.write(response)
