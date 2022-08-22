"""Module utils provides helper functions for a clean program flow."""
from __future__ import annotations
import json

def optimize_filters(available_filters: list[dict], total_items: int) -> list[dict]:
    """Returns a list of filters whose result
    is not equal to the total number of items.
        Args:
            available_filters:
            total_items:
        Returns:
            A list of dict
    """
    optimized_filters = []
    for available_filter in available_filters:
        values = []
        for value in available_filter['values']:
            if value['results'] < total_items:
                values.append(value)
        if values:
            available_filter['values'] = values
            optimized_filters.append(available_filter)
    return optimized_filters

def get_filter_combinations(available_filters: list[dict], available_sorts: list[dict]) -> list[dict]:
    """Returns a list of dictionaries representing filters (KeyValuePairs).
        Args:
            available_filters:
            available_sorts:
        Returns:
            A list of dict
    """
    filters = []
    for available_filter in available_filters:
        for value in available_filter['values']:
            filters.append({available_filter['id']: value['id']})

    sorts = []
    for available_sort in available_sorts:
        sorts.append({'sort': available_sort['id']})

    combo = [{**f,**s} for s in sorts for f in filters]
    
    return combo

def format_items(items, today):
    """Returns a list of tuples with site_id, item_id, last_run, category_id and item_json.
        Args:
            items:
            today: 
        Returns:
            A list of tuple
    """
    records = []
    for item in items:
        site_id = item['site_id']
        item_id = item['id'][3:]
        category_id = item['category_id'][3:]
        last_run = today
        item_json = json.dumps(item)
        records.append((site_id, item_id, last_run, category_id, item_json))
    return records


def format_categories(categories:list, today:str) -> list[tuple]:
    """Returns a list of tuples with site_id, category_id, last_run and category_json.
    Args:
        categories:
        today:
    Returns a list of tuples
    """
    formated = []
    for category in categories:
        site_id = category['id'][0:3]
        category_id = category['id'][3:]
        last_run = today
        category_json = json.dumps(category)
        formated.append((site_id, category_id, last_run, category_json))
    return formated
