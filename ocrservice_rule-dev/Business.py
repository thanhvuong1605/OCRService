import numpy as np
from StringHelper import StringHelper

class Business:
    @staticmethod
    def normalize_blocks(blocks):
        res = []
        for block in blocks:
            if len(block) != 0:
                res.append(block)
        return res
    @staticmethod
    def get_result(features, blocks, rules, CONFIDENCE_VALUE = 0.75):
        if CONFIDENCE_VALUE is None:
            CONFIDENCE_VALUE = 0.75
        res = {}
        blocks = Business.normalize_blocks(blocks)
        for i in range(len(blocks)):
            blocks[i] = StringHelper.normalize_str(blocks[i])
        
        bot_rule = False
        top_rule = False
        
        bot_rule = "bot_rule" in rules
        top_rule = "top_rule" in rules
        
        if bot_rule:
            blocks.append("")
        if top_rule:
            blocks = [""] + blocks
        feature_size = len(features)
        block_size = len(blocks)
        
        for i in range(feature_size):
            feature = features[i]
            for j in range(block_size):
                block = blocks[j]                
                id = StringHelper.is_contain(block, feature, CONFIDENCE_VALUE)
                if id != -1:
                    if len(block[id:]) > len(feature) + 1:
                        id += len(feature)
                        min_id = len(block)
                        for fea in features:
                            tmp_id = StringHelper.is_contain(block[id:], fea)
                            if tmp_id != -1: 
                                min_id = np.min([min_id, tmp_id])
                        res[feature] = block[id: id + min_id]
                    elif bot_rule == True:
                        res[feature] = blocks[j + 1]
                    elif top_rule == True:
                        res[feature] = blocks[j - 1]
                    break
        for fea in res:
            res[fea] = StringHelper.normalize_result(res[fea])
        return res
