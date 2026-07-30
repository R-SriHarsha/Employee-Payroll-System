def calculate_salary(base_salary, present_days, month_days=30):
    per_day = base_salary / month_days
    effective_base = per_day * present_days

    hra = 0.3 * effective_base
    da = 0.05 * effective_base

    gross = effective_base + hra + da

    pf = min(0.12 * effective_base, 1800)
    tax = 0.05 * gross

    net_salary = gross - (pf + tax)

    return {
        "basic": effective_base,
        "hra": hra,
        "da": da,
        "pf": pf,
        "tax": tax,
        "gross": gross,
        "net": net_salary
    }
