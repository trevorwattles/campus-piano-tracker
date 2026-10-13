from db import run_select
from llm import Usage, chat, extract_sql
from prompts import build_answer_prompt, build_sql_prompt


def ask(question, strategy):
    """question -> SQL -> rows -> friendly answer. Never raises; errors go in the result."""
    usage = Usage()
    result = {"question": question, "strategy": strategy, "sql": None,
              "columns": [], "rows": [], "answer": None, "error": None}
    try:
        prompt = build_sql_prompt(strategy, question)
        sql = extract_sql(chat([{"role": "user", "content": prompt}], usage))
        result["sql"] = sql
        try:
            columns, rows = run_select(sql)
        except Exception as err:
            # one retry: show the model its own error
            retry = [{"role": "user", "content": prompt},
                     {"role": "assistant", "content": sql},
                     {"role": "user", "content": f"That failed with: {err}. Give a corrected sqlite select statement only."}]
            sql = extract_sql(chat(retry, usage))
            result["sql"] = sql
            columns, rows = run_select(sql)
        result.update(sql=sql, columns=columns, rows=rows)
        result["answer"] = chat([{"role": "user", "content": build_answer_prompt(question, sql, columns, rows)}], usage)
    except Exception as err:
        result["error"] = str(err)
    result["tokens"] = {"input": usage.input, "output": usage.output}
    result["cost_usd"] = round(usage.cost, 6)
    return result
