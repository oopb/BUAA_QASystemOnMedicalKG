#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-5

from py2neo import Graph


class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "CCX790625843"))
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            subject = answers[0]['m.name']

            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            subject = answers[0]['m.name']
            final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(
                list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject,
                                                                        '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject,
                                                                       '；'.join(list(set(desc))[:self.num_limit]))
        # 药品生产商
        elif question_type == 'drug_producer':
            drug = answers[0]['d.name'] if 'd.name' in answers[0] else ''
            producers = [i['p.name'] for i in answers]
            final_answer = '{0}的生产商有：{1}'.format(drug, '；'.join(list(set(producers))[:self.num_limit]))

        # 某病能否吃某食物
        elif question_type == 'disease_food_can_eat':
            final_answer = '患有{0}的人最好不要吃{1}\n'.format(answers[0]['d.name'], '，'.join(
                i['f.name'] for i in answers))
            # 判断是否有禁忌
            for i in answers:
                if i['r_type'] == 'no_eat':
                    final_answer += '得{0}时不能吃{1}'.format(i['d.name'], i['qf'])
                    break
            else:
                if answers:
                    final_answer += '得{0}时可以吃{1}'.format(answers[0]['d.name'], answers[0]['qf'])
                else:
                    final_answer += '未找到相关饮食禁忌信息'

        # 比较两食物忌口疾病数量
        elif question_type == 'food_not_disease_compare':
            if len(answers) >= 2:
                food1 = answers[0]['f.name']
                count1 = answers[0]['count1']
                food2 = answers[1]['f.name']
                count2 = answers[1]['count2']
                if count1 > count2:
                    final_answer = '需要忌吃{0}的病更多（{1}种），需要忌吃{2}的病有{3}种'.format(food1, count1, food2,
                                                                                              count2)
                elif count2 > count1:
                    final_answer = '需要忌吃{0}的病更多（{1}种），需要忌吃{2}的病有{3}种'.format(food2, count2, food1,
                                                                                              count1)
                else:
                    final_answer = '需要忌吃{0}和{1}的病数量相同（{2}种）'.format(food1, food2, count1)

        # 比较两药品生产商数量
        elif question_type == 'drug_producer_compare':
            if len(answers) >= 2:
                drug1 = answers[0]['d.name']
                count1 = answers[0]['count1']
                drug2 = answers[1]['d.name']
                count2 = answers[1]['count2']
                if count1 > count2:
                    final_answer = '{0}的生产商数量更多（{1}家），{2}有{3}家'.format(drug1, count1, drug2, count2)
                elif count2 > count1:
                    final_answer = '{0}的生产商数量更多（{1}家），{2}有{3}家'.format(drug2, count2, drug1, count1)
                else:
                    final_answer = '{0}和{1}的生产商数量相同（{2}家）'.format(drug1, drug2, count1)

        # 易感疾病检查
        elif question_type == 'disease_easyget_check':
            res = []
            for i in answers:
                res.append('{0}的易感疾病{1}建议检查：{2}'.format(i['d.name'], i['ad.name'], i['c.name']))
            final_answer = '\n'.join(res[:self.num_limit])

        # 易感疾病预防
        elif question_type == 'disease_easyget_prevent':
            res = []
            for i in answers:
                res.append('{0}的易感疾病{1}建议预防措施：{2}'.format(i['d.name'], i['ad.name'], i['ad.prevent']))
            final_answer = '\n'.join(res[:self.num_limit])

        elif question_type == 'child_easyget_prevent':
            res = []
            for i in answers:
                res.append('{0}（{1}）建议预防措施：{2}'.format(i['d.name'], i['d.easy_get'], i['d.prevent']))
            final_answer = '\n'.join(res[:self.num_limit])

        # 药商还会生产哪些药品
        elif question_type == 'producer_other_drug':
            producers = set(i['p.name'] for i in answers)
            lines = []
            for producer in producers:
                other_drugs = [i['other_name'] for i in answers if i['p.name'] == producer and i['other_name']]
                if other_drugs:
                    for drug in set(other_drugs):
                        lines.append('{0}还生产：{1}'.format(producer, drug))
            if len(lines) == 0:
                lines.append('不生产其余药品')
            final_answer = '\n'.join(lines)

        # 并发症属于哪个科室
        elif question_type == 'disease_acompany_department':
            res = []
            for i in answers:
                res.append('{0}属于{1}'.format(i['d2.name'], i['d2.cure_department']))
            final_answer = '并发症及其科室如下：\n' + '\n'.join(res[:self.num_limit])

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
