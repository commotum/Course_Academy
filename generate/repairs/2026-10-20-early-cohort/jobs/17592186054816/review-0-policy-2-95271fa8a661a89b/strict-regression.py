import json
r=json.load(open("minimal-cli.json"))[0]
q=r["question"]
f=q[":question/answer-fields"][-1]
assert f[":answer-field/key"]=="None of the above"
assert "leave every box unchecked" not in q[":question/worked-solution"], "Explicit None must be selected, but solution tells learner to leave every box unchecked"
