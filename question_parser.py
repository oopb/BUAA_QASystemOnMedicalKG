#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:
    '''构建实体节点'''

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''

    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_acompany':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'food_not_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'food_do_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_producer':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_food_can_eat':
                diseases = entity_dict.get('disease', [])
                foods = entity_dict.get('food', [])
                sql = self.sql_transfer(question_type, (diseases, foods))

            elif question_type == 'food_not_disease_compare':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'drug_producer_compare':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_easyget_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'child_easyget_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('child'))

            elif question_type == 'producer_other_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_acompany_department':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'disease_lasttime':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(i) for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'disease_cureprob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]

        # 查询疾病的易发人群
        elif question_type == 'disease_easyget':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]

        # 查询疾病的并发症
        elif question_type == 'disease_acompany':
            sql1 = [
                "MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2
        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i)
                   for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            sql1 = [
                "MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i)
                for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2

        # 已知忌口查疾病
        elif question_type == 'food_not_disease':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i)
                   for i in entities]

        # 已知推荐查疾病
        elif question_type == 'food_do_disease':
            sql1 = [
                "MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i)
                for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            sql1 = [
                "MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql1 = [
                "MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2
        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = [
                "MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            sql = [
                "MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]

        # 药品生产商
        elif question_type == 'drug_producer':
            sql = ["MATCH (p:Producer)-[:drugs_of]->(d:Drug) WHERE d.name = '{0}' RETURN d.name, p.name".format(i) for i
                   in entities]

        # 某病能否吃某食物
        elif question_type == 'disease_food_can_eat':
            diseases, foods = entities
            if not diseases or not foods:
                return []
            sql = [
                "MATCH (d:Disease)-[r:no_eat]->(f:Food) WHERE d.name = '{0}' RETURN d.name, '{1}' as qf, CASE WHEN f.name = '{1}' THEN type(r) ELSE '' END as r_type, f.name".format(
                    d, f)
                for d in diseases for f in foods
            ]

        # 比较两食物忌口疾病数量
        elif question_type == 'food_not_disease_compare':
            if len(entities) < 2:
                return []
            food1, food2 = entities[0], entities[1]
            sql1 = [
                "MATCH (d:Disease)-[r:no_eat]->(f:Food) WHERE f.name = '{0}' RETURN f.name, count(d) as count1".format(
                    food1),
            ]
            sql2 = [
                "MATCH (d:Disease)-[r:no_eat]->(f:Food) WHERE f.name = '{0}' RETURN f.name, count(d) as count2".format(
                    food2)
            ]
            sql = sql1 + sql2

        # 比较两药品生产商数量
        elif question_type == 'drug_producer_compare':
            if len(entities) < 2:
                return []
            drug1, drug2 = entities[0], entities[1]
            sql1 = [
                "MATCH (p:Producer)-[r:drugs_of]->(d:Drug) WHERE d.name = '{0}' RETURN d.name, count(p) as count1".format(
                    drug1)
            ]
            sql2 = [
                "MATCH (p:Producer)-[r:drugs_of]->(d:Drug) WHERE d.name = '{0}' RETURN d.name, count(p) as count2".format(
                    drug2)
            ]
            sql = sql1 + sql2

        # 易感疾病检查
        elif question_type == 'disease_easyget_check':
            sql = [
                "MATCH (d:Disease)-[r1:acompany_with]->(ad:Disease)-[r2:need_check]->(c:Check) WHERE d.name = '{0}' RETURN d.name, ad.name, c.name".format(
                    i)
                for i in entities
            ]

        # 易感疾病预防
        elif question_type == 'disease_easyget_prevent':
            sql = [
                "MATCH (d:Disease)-[r:acompany_with]->(ad:Disease) WHERE d.name = '{0}' RETURN d.name, ad.name, ad.prevent".format(
                    i)
                for i in entities
            ]
        elif question_type == 'child_easyget_prevent':
            sql1 = ["MATCH (d:Disease) WHERE d.easy_get = '好发于新生儿' RETURN d.name, d.easy_get, d.prevent"]
            sql2 = ["MATCH (d:Disease) WHERE d.easy_get = '发生于5岁以下儿童' RETURN d.name, d.easy_get, d.prevent"]
            sql3 = ["MATCH (d:Disease) WHERE d.easy_get = '多见于小儿' RETURN d.name, d.easy_get, d.prevent"]
            sql = sql1 + sql2 + sql3

        # 药商还会生产哪些药品
        elif question_type == 'producer_other_drug':
            sql = [
                "MATCH (p:Producer)-[:drugs_of]->(d:Drug) WHERE d.name = '{0}' WITH p MATCH (p)-[:drugs_of]->(other:Drug) RETURN p.name, CASE WHEN other.name <> '{0}' THEN other.name ELSE '' END as other_name".format(
                    i)
                for i in entities
            ]

        # 并发症属于哪个科室
        elif question_type == 'disease_acompany_department':
            sql = [
                "MATCH (d1:Disease)-[:acompany_with]->(d2:Disease) WHERE d1.name = '{0}' RETURN d2.name, d2.cure_department".format(
                    i)
                for i in entities
            ]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
