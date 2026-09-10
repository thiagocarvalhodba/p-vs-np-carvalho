import json
import numpy as np

with open('Fontes/exp_clg04_audit_log.json', 'r') as f:
    records = json.load(f)

# Group by (n, family, dynamics, rep_type)
groups = {}
for r in records:
    k = (r['n'], r['family'], r['dynamics'], r['rep_type'])
    groups.setdefault(k, []).append(r)

print('=' * 110)
print(f"{'Grupo Experimental':<42} | {'R_traj':<10} | {'R_inst (Media +/- SEM)':<24} | {'dH (Media +/- SEM)':<18}")
print('=' * 110)

hierarchical_summary = {}

for k in sorted(groups.keys()):
    recs = groups[k]
    n, fam, dyn, rep = k
    inst_ids = sorted(list(set(r['instance_id'] for r in recs)))
    r_insts = []
    dh_insts = []
    for i_id in inst_ids:
        i_recs = [r for r in recs if r['instance_id'] == i_id]
        succ = sum(1 for r in i_recs if r['reached'])
        r_insts.append(succ / len(i_recs))
        dh_insts.append(np.mean([r['normalized_hamming_dist'] for r in i_recs]))
        
    r_traj = sum(1 for r in recs if r['reached']) / len(recs)
    r_mean = float(np.mean(r_insts))
    r_sem = float(np.std(r_insts, ddof=1) / np.sqrt(len(r_insts)))
    dh_mean = float(np.mean(dh_insts))
    dh_sem = float(np.std(dh_insts, ddof=1) / np.sqrt(len(dh_insts)))
    
    group_str = f"N={n} | {fam[:10]} | {dyn:<8} | {rep}"
    r_inst_str = f"{r_mean*100:5.1f}% +/- {r_sem*100:4.1f}%"
    dh_str = f"{dh_mean:.3f} +/- {dh_sem:.3f}"
    print(f"{group_str:<42} | {r_traj*100:5.1f}%     | {r_inst_str:<24} | {dh_str}")
    
    hierarchical_summary[f"N{n}_{fam}_{dyn}_{rep}"] = {
        "n": n, "family": fam, "dynamics": dyn, "rep": rep,
        "r_traj": r_traj,
        "r_inst_mean": r_mean, "r_inst_sem": r_sem, "r_inst_per_instance": r_insts,
        "dh_mean": dh_mean, "dh_sem": dh_sem, "dh_per_instance": dh_insts
    }

print('=' * 110)

with open('Fontes/exp_clg04_hierarchical_summary.json', 'w') as f:
    json.dump(hierarchical_summary, f, indent=2)
print("Salvo: Fontes/exp_clg04_hierarchical_summary.json")
