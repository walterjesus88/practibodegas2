import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sqlalchemy.orm import Session
#from .models import ReglaApriori
from datetime import datetime
#import json

from .models import ReglaAprioriRun, ReglaAprioriRule

# recibe un dataframe o una sesión para leer de BD

def run_apriori_from_df(df: pd.DataFrame, min_support=0.002, min_confidence=0.05):
    # df expected: columns: id_venta, producto
    print('DF INPUT')
    print(df)

    pivot = (df.assign(val=1)
            .pivot_table(index='ticket_id', columns='producto', values='val', fill_value=0)
            .astype(bool))

    print('pivottt')
    print(pivot)
    frequent = apriori(pivot, min_support=min_support, use_colnames=True)
    print('FREQUENT ITEMSETS')
    print(frequent)
    rules = association_rules(frequent, metric='confidence', min_threshold=min_confidence)
    print('ASSOCIATION RULES')
    print(rules)
    # simplificar salida
    rules = rules[['antecedents','consequents','support','confidence','lift']]
    # convert sets to lists
    print('RULES DF')
    print(rules)
        
    rules['antecedents'] = rules['antecedents'].apply(lambda s: list(s))
    rules['consequents'] = rules['consequents'].apply(lambda s: list(s))
    return rules.to_dict(orient='records')

# def save_rules(session: Session, rules, params):
#     r = ReglaApriori(created_at=datetime.utcnow(), params=params, rules_json=rules)
#     session.add(r)
#     session.commit()
#     return r.id


def save_rules(session: Session, rules, params):
    run = ReglaAprioriRun(
        created_at=datetime.utcnow(),
        params=params
    )
    session.add(run)
    session.commit()
    session.refresh(run)

    for rule in rules:
        r = ReglaAprioriRule(
            run_id=run.id,
            antecedents=list(rule['antecedents']),
            consequents=list(rule['consequents']),
            support=float(rule['support']),
            confidence=float(rule['confidence']),
            lift=float(rule['lift']),
        )
        session.add(r)

    session.commit()
    return run.id
