"""Negative-XP attempts require a perfect capture retake, without touching learner state."""
import json
import re

from core import atomic_json


def earned_xp(completion):
    loss = re.search(r'(?:lost\s+|penalty\s+(?:of\s+)?)(-?\d+)\s*XP',completion,re.I)
    if loss:
        return -abs(int(loss[1]))
    if re.search(r'No XP were awarded\.',completion,re.I):
        return 0
    award = re.search(r'(?:awarded|earned)\s+(-?\d+)(?:\s+of\b.{0,50}?)?\s*XP',completion,re.I)
    return int(award[1]) if award else None


def completion_outcome(completion,kind):
    """Recognize the player's terminal messages, including failed attempts."""
    if kind not in ('lesson','review'):
        return None
    if (re.search(r'\b(?:This|The)\s+' + re.escape(kind) +
                  r'\s+has been halted due to poor performance(?: and has been assigned a penalty)?\.',
                  completion, re.I) or
        f"You didn't pass the {kind}, however, you were awarded a limited amount of XP" in completion):
        return 'failed'
    if 'completed the '+kind in completion.lower():
        return 'passed'
    return None


def update_policy(state_dir, outcomes=(), completed_state=None):
    path = state_dir/'perfect-retakes.json'
    policy = json.loads(path.read_text()) if path.exists() else {'seen_failures':[], 'pending':{}}
    if completed_state is not None:
        kind, topic = completed_state.get('task_type','lesson'), completed_state.get('topic_id')
        xp = completed_state.get('earned_xp')
        if kind in ('lesson','review') and topic is not None:
            key = kind+':'+str(topic)
            if xp is not None and xp < 0:
                outcomes = [*outcomes,{'task_id':completed_state['task_id'],'task_type':kind,'topic_id':topic,'earned_xp':xp}]
            elif (completed_state.get('activity_complete') and completed_state.get('answer_policy') == 'all_correct' and
                  completed_state.get('questions') and
                  all(q.get('actual_result') == 'Correct' for q in completed_state['questions'].values())):
                policy['pending'].pop(key,None)
    for outcome in sorted(outcomes,key=lambda o:o['task_id']):
        if (outcome.get('task_type') not in ('lesson','review') or outcome.get('topic_id') is None or
            outcome.get('earned_xp',0) >= 0 or outcome['task_id'] in policy['seen_failures']):
            continue
        policy['seen_failures'].append(outcome['task_id'])
        policy['pending'][outcome['task_type']+':'+str(outcome['topic_id'])] = outcome
    atomic_json(path,policy)
    return policy


def apply_policy(activity, policy):
    if activity is not None and activity.get('task_type') in ('lesson','review'):
        failed = policy['pending'].get(activity['task_type']+':'+str(activity['topic_id']))
        if failed:
            return {**activity,'answer_policy':'all_correct','perfect_retake_of':failed['task_id']}
    return activity
