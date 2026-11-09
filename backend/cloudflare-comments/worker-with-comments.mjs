const HEART_COMMENT_RISK_IDS = {"G_INT_ALLOC":3,"G_INT_ALLOC_001":4,"G_INT_ALLOC_002":4,"G_INT_ALLOC_003":4,"G_INT_ALLOC_004":4,"G_INT_ALLOC_005":4,"G_INT_ALLOC_006":4,"G_INT_ALLOC_007":4,"G_INT_ALLOC_009":4,"G_INT_ALLOC_010":4,"G_INT_ALLOC_012":4,"G_INT_ALLOC_013":4,"G_INT_ALLOC_015":4,"G_INT_ANTH":3,"G_INT_ANTH_001":4,"G_INT_ANTH_002":4,"G_INT_ANTH_003":4,"G_INT_ANTH_004":4,"G_INT_ANTH_005":4,"G_INT_ANTH_006":4,"G_INT_COPY":3,"G_INT_COPY_001":4,"G_INT_COPY_002":4,"G_INT_COPY_003":4,"G_INT_COPY_006":4,"G_INT_COPY_007":4,"G_INT_COPY_009":4,"G_INT_ILLEGAL":3,"G_INT_ILLEGAL_001":4,"G_INT_ILLEGAL_003":4,"G_INT_ILLEGAL_006":4,"G_INT_ILLEGAL_007":4,"G_INT_ILLEGAL_008":4,"G_INT_ILLEGAL_009":4,"G_INT_ILLEGAL_010":4,"G_INT_ILLEGAL_011":4,"G_INT_ILLEGAL_013":4,"G_INT_ILLEGAL_014":4,"G_INT_ILLEGAL_015":4,"G_INT_ILLEGAL_016":4,"G_INT_ILLEGAL_019":4,"G_INT_ILLEGAL_020":4,"G_INT_ILLEGAL_021":4,"G_INT_ILLEGAL_022":4,"G_INT_ILLEGAL_023":4,"G_INT_POL":3,"G_INT_POL_001":4,"G_INT_POL_002":4,"G_INT_POL_003":4,"G_INT_POL_005":4,"G_INT_POL_006":4,"G_INT_POL_007":4,"G_INT_POL_008":4,"G_INT_PRIV":3,"G_INT_PRIV_001":4,"G_INT_PRIV_002":4,"G_INT_PRIV_003":4,"G_INT_PRIV_005":4,"G_INT_PRIV_007":4,"G_INT_PRIV_008":4,"G_INT_PRIV_009":4,"G_INT_PRIV_010":4,"G_INT_PRIV_012":4,"G_INT_PRIV_014":4,"G_INT_PRIV_015":4,"G_INT_PRIV_016":4,"G_INT_PRIV_017":4,"G_INT_PRIV_018":4,"G_INT_PRIV_019":4,"G_INT_PRIV_020":4,"G_INT_PRIV_021":4,"G_INT_PRIV_022":4,"G_INT_PRIV_024":4,"G_INT_PRIV_025":4,"G_INT_PRIV_027":4,"G_INT_PRIV_028":4,"G_INT_PRIV_029":4,"G_INT_PRIV_030":4,"G_INT_PRIV_031":4,"G_INT_REL":3,"G_INT_REL_001":4,"G_INT_REL_002":4,"G_INT_REL_004":4,"G_INT_REL_006":4,"G_INT_REL_007":4,"G_INT_REL_008":4,"G_INT_REPR":3,"G_INT_REPR_001":4,"G_INT_REPR_002":4,"G_INT_REPR_003":4,"G_INT_REPR_004":4,"G_INT_REPR_006":4,"G_INT_REPR_007":4,"G_INT_REPR_009":4,"G_INT_REPR_010":4,"G_INT_REPR_011":4,"G_INT_REPR_012":4,"G_INT_REPR_013":4,"G_INT_REPR_014":4,"G_INT_REPR_015":4,"G_INT_REPR_016":4,"G_INT_REPR_017":4,"G_INT_REPR_018":4,"G_INT_REPR_019":4,"G_INT_REPR_020":4,"G_INT_REPR_021":4,"G_INT_REPR_022":4,"G_INT_REPR_023":4,"G_INT_REPR_024":4,"G_INT_REPR_025":4,"G_INT_REPR_026":4,"G_INT_REPR_027":4,"G_INT_REPR_028":4,"G_INT_REPR_029":4,"G_INT_REPR_032":4,"G_INT_REPR_033":4,"G_INT_SELF":3,"G_INT_SELF_001":4,"G_INT_SELF_003":4,"G_INT_SELF_004":4,"G_INT_SELF_005":4,"G_INT_SELF_007":4,"G_INT_SELF_008":4,"G_INT_SEX":3,"G_INT_SEX_002":4,"G_INT_SEX_003":4,"G_INT_SEX_004":4,"G_INT_SEX_005":4,"G_INT_SEX_007":4,"G_INT_SEX_008":4,"G_INT_SEX_009":4,"G_INT_SEX_010":4,"G_INT_UNETH":3,"G_INT_UNETH_002":4,"G_INT_UNETH_003":4,"G_INT_UNETH_004":4,"G_INT_UNETH_005":4,"G_INT_UNETH_007":4,"G_INT_UNETH_008":4,"G_INT_UNETH_010":4,"G_INT_UNETH_011":4,"G_INT_UNETH_012":4,"G_INT_UNETH_014":4,"G_INT_UNETH_015":4,"G_INT_UNETH_017":4,"G_INT_UNETH_019":4,"G_INT_UNETH_020":4,"G_INT_UNETH_021":4,"G_INT_UNETH_022":4,"G_INT_UNETH_024":4,"G_INT_UNETH_026":4,"G_INT_UNETH_027":4,"G_INT_UNETH_028":4,"G_INT_UNETH_029":4,"G_INT_UNETH_030":4,"G_INT_UNETH_031":4,"G_INT_UNETH_032":4,"G_INT_UNETH_033":4,"G_INT_VALUE":3,"G_INT_VALUE_002":4,"G_INT_VALUE_004":4,"G_INT_VALUE_006":4,"G_INT_VALUE_007":4,"G_INT_VALUE_010":4,"G_INT_VALUE_012":4,"G_INT_VALUE_013":4,"G_INT_VALUE_014":4,"G_INT_VALUE_015":4,"G_INT_VALUE_016":4,"G_INT_VALUE_018":4,"G_INT_VALUE_019":4,"G_INT_VALUE_020":4,"G_INT_VALUE_022":4,"G_INT_VALUE_024":4,"G_INT_VALUE_025":4,"G_INT_VIOL":3,"G_INT_VIOL_001":4,"G_INT_VIOL_002":4,"G_INT_VIOL_004":4,"G_INT_VIOL_005":4,"G_INT_VIOL_006":4,"G_INT_VIOL_007":4,"G_INT_VIOL_008":4,"G_INT_VIOL_009":4,"G_INT_VIOL_010":4,"G_INT_VIOL_011":4,"G_INT_VIOL_012":4,"G_INT_WEAP":3,"G_INT_WEAP_002":4,"G_INT_WEAP_003":4,"G_INT_WEAP_006":4,"G_INT_WEAP_009":4,"G_INT_WEAP_010":4,"G_INT_WEAP_011":4,"G_INT_WEAP_014":4,"G_INT_WEAP_016":4,"G_INT_WEAP_018":4,"G_INT_WEAP_021":4,"G_INT_WEAP_022":4,"G_INT_WEAP_023":4,"G_INT_WEAP_024":4,"G_INT_WEAP_025":4,"G_INT_WEAP_026":4,"G_INT_WEAP_027":4,"G_INT_WEAP_029":4,"G_INT_WEAP_030":4,"G_INT_WEAP_032":4,"G_SOC_CULT":3,"G_SOC_CULT_001":4,"G_SOC_CULT_002":4,"G_SOC_CULT_005":4,"G_SOC_CULT_007":4,"G_SOC_CULT_008":4,"G_SOC_CULT_009":4,"G_SOC_CULT_010":4,"G_SOC_CULT_011":4,"G_SOC_CULT_012":4,"G_SOC_CULT_014":4,"G_SOC_CULT_016":4,"G_SOC_CULT_017":4,"G_SOC_CULT_018":4,"G_SOC_CULT_019":4,"G_SOC_CULT_020":4,"G_SOC_CULT_021":4,"G_SOC_CULT_022":4,"G_SOC_CULT_023":4,"G_SOC_CULT_024":4,"G_SOC_DEMOC":3,"G_SOC_DEMOC_001":4,"G_SOC_DEMOC_002":4,"G_SOC_DEMOC_003":4,"G_SOC_DEMOC_005":4,"G_SOC_DEMOC_006":4,"G_SOC_DEMOC_007":4,"G_SOC_DEMOC_008":4,"G_SOC_DEMOC_010":4,"G_SOC_DEMOC_011":4,"G_SOC_ECON":3,"G_SOC_ECON_001":4,"G_SOC_ECON_002":4,"G_SOC_ECON_003":4,"G_SOC_ECON_005":4,"G_SOC_ECON_006":4,"G_SOC_ECON_008":4,"G_SOC_ECON_010":4,"G_SOC_ECON_012":4,"G_SOC_ENV":3,"G_SOC_ENV_001":4,"G_SOC_ENV_002":4,"G_SOC_ENV_003":4,"G_SOC_ENV_005":4,"G_SOC_ENV_007":4,"G_SOC_ENV_008":4,"G_SOC_ENV_009":4,"G_SOC_ENV_011":4,"G_SOC_ENV_012":4,"G_SOC_GOV":3,"G_SOC_GOV_002":4,"G_SOC_GOV_005":4,"G_SOC_GOV_006":4,"G_SOC_GOV_008":4,"G_SOC_GOV_009":4,"G_SOC_GOV_010":4,"G_SOC_GOV_011":4,"G_SOC_GOV_015":4,"G_SOC_GOV_016":4,"G_SOC_GOV_017":4,"G_SOC_GOV_020":4,"G_SOC_GOV_021":4,"G_SOC_GOV_022":4,"G_SOC_GOV_023":4,"G_SOC_GOV_024":4,"G_SOC_GOV_025":4,"G_SOC_GOV_026":4,"G_SOC_GOV_027":4,"G_SOC_GOV_029":4,"G_SOC_GOV_030":4,"G_SOC_GOV_033":4,"G_SOC_GOV_034":4,"G_SOC_GOV_035":4,"G_SOC_GOV_036":4,"G_SOC_GOV_039":4,"G_SOC_GOV_040":4,"G_SOC_GOV_041":4,"G_SOC_GOV_042":4,"G_SOC_GOV_043":4,"G_SOC_GOV_044":4,"G_SOC_GOV_045":4,"G_SOC_GOV_046":4,"G_SOC_POWER":3,"G_SOC_POWER_001":4,"G_SOC_POWER_002":4,"G_SOC_POWER_003":4,"G_SOC_POWER_004":4,"G_SOC_POWER_005":4,"G_SOC_POWER_006":4,"G_SOC_POWER_007":4,"G_SOC_POWER_008":4,"G_SOC_POWER_010":4,"G_SOC_POWER_012":4,"G_SOC_POWER_015":4,"G_SOC_POWER_017":4,"G_SOC_POWER_018":4,"G_SOC_POWER_019":4,"G_SOC_POWER_023":4,"G_SOC_POWER_025":4,"G_SOC_POWER_026":4,"G_SOC_POWER_027":4,"G_SOC_POWER_028":4,"G_SYS_CONTEST":3,"G_SYS_CONTEST_001":4,"G_SYS_CONTEST_002":4,"G_SYS_CONTEST_003":4,"G_SYS_CONTEST_004":4,"G_SYS_CONTEXT":3,"G_SYS_CONTEXT_001":4,"G_SYS_CONTEXT_002":4,"G_SYS_CONTEXT_003":4,"G_SYS_CONTEXT_004":4,"G_SYS_CONTEXT_005":4,"G_SYS_CONTEXT_006":4,"G_SYS_CONTEXT_007":4,"G_SYS_CONTEXT_008":4,"G_SYS_CONTEXT_009":4,"G_SYS_CONTEXT_011":4,"G_SYS_CONTEXT_012":4,"G_SYS_CONTEXT_013":4,"G_SYS_EVAL":3,"G_SYS_EVAL_001":4,"G_SYS_EVAL_002":4,"G_SYS_EVAL_003":4,"G_SYS_EVAL_004":4,"G_SYS_EVAL_005":4,"G_SYS_EVAL_006":4,"G_SYS_EVAL_007":4,"G_SYS_EVAL_008":4,"G_SYS_EVAL_009":4,"G_SYS_EVAL_012":4,"G_SYS_EVAL_013":4,"G_SYS_EVAL_014":4,"G_SYS_EVAL_016":4,"G_SYS_EVAL_017":4,"G_SYS_EVAL_019":4,"G_SYS_EVAL_021":4,"G_SYS_EVAL_022":4,"G_SYS_EVAL_023":4,"G_SYS_EVAL_024":4,"G_SYS_EVAL_025":4,"G_SYS_EVAL_026":4,"G_SYS_EVAL_027":4,"G_SYS_EVAL_028":4,"G_SYS_EVAL_029":4,"G_SYS_EVAL_031":4,"G_SYS_EVAL_032":4,"G_SYS_EVAL_033":4,"G_SYS_EVAL_035":4,"G_SYS_EVAL_036":4,"G_SYS_EVAL_037":4,"G_SYS_EVAL_038":4,"G_SYS_EVAL_039":4,"G_SYS_EVAL_040":4,"G_SYS_EVAL_041":4,"G_SYS_EVAL_042":4,"G_SYS_EVAL_043":4,"G_SYS_EVAL_044":4,"G_SYS_EVAL_045":4,"G_SYS_EVAL_046":4,"G_SYS_EVAL_048":4,"G_SYS_EVAL_052":4,"G_SYS_EVAL_054":4,"G_SYS_EVAL_060":4,"G_SYS_EVAL_062":4,"G_SYS_EVAL_065":4,"G_SYS_EVAL_066":4,"G_SYS_EVAL_068":4,"G_SYS_EVAL_069":4,"G_SYS_EVAL_070":4,"G_SYS_EVAL_071":4,"G_SYS_EVAL_072":4,"G_SYS_EVAL_073":4,"G_SYS_EVAL_074":4,"G_SYS_EVAL_077":4,"G_SYS_INCONS":3,"G_SYS_INCONS_001":4,"G_SYS_INCONS_002":4,"G_SYS_INCONS_003":4,"G_SYS_INPUT":3,"G_SYS_INPUT_001":4,"G_SYS_INPUT_002":4,"G_SYS_INPUT_003":4,"G_SYS_MISINFO":3,"G_SYS_MISINFO_002":4,"G_SYS_MISINFO_003":4,"G_SYS_MISINFO_004":4,"G_SYS_MISINFO_006":4,"G_SYS_MISINFO_007":4,"G_SYS_MISINFO_008":4,"G_SYS_MISINFO_009":4,"G_SYS_MISINFO_010":4,"G_SYS_MISINFO_011":4,"G_SYS_MISINFO_012":4,"G_SYS_MISINFO_013":4,"G_SYS_MISINFO_015":4,"G_SYS_MISINFO_016":4,"G_SYS_MISINFO_017":4,"G_SYS_MISINFO_018":4,"G_SYS_MISINFO_019":4,"G_SYS_MISINFO_021":4,"G_SYS_MISINFO_022":4,"G_SYS_MISINFO_023":4,"G_SYS_OEXT":3,"G_SYS_OEXT_001":4,"G_SYS_OEXT_006":4,"G_SYS_OEXT_007":4,"G_SYS_OEXT_008":4,"G_SYS_OEXT_009":4,"G_SYS_OEXT_013":4,"G_SYS_OEXT_014":4,"G_SYS_OREF":3,"G_SYS_OREF_001":4,"G_SYS_OREF_002":4,"G_SYS_OREF_003":4,"G_SYS_OVERCONF":3,"G_SYS_OVERCONF_001":4,"G_SYS_OVERCONF_002":4,"G_SYS_OVERCONF_003":4,"G_SYS_OVERCONF_004":4,"G_SYS_OVERCONF_006":4,"G_SYS_PERF":3,"G_SYS_PERF_001":4,"G_SYS_PERF_002":4,"G_SYS_PERF_003":4,"G_SYS_PERF_004":4,"G_SYS_PERF_005":4,"G_SYS_PERF_006":4,"G_SYS_PERF_007":4,"G_SYS_PERF_008":4,"G_SYS_PERF_009":4,"G_SYS_PERF_010":4,"G_SYS_PERF_011":4,"G_SYS_PERF_012":4,"G_SYS_PERF_013":4,"G_SYS_PERF_014":4,"G_SYS_PERF_016":4,"G_SYS_PERF_017":4,"G_SYS_PERF_018":4,"G_SYS_PERF_019":4,"G_SYS_PERF_020":4,"G_SYS_PERF_021":4,"G_SYS_POLICY":3,"G_SYS_POLICY_001":4,"G_SYS_POLICY_002":4,"G_SYS_POLICY_003":4,"G_SYS_POLICY_004":4,"G_SYS_POLICY_005":4,"G_SYS_POLICY_006":4,"G_SYS_POLICY_008":4,"G_SYS_POLICY_009":4,"G_SYS_POLICY_010":4,"G_SYS_SECADV":3,"G_SYS_SECADV_001":4,"G_SYS_SECADV_002":4,"G_SYS_SECADV_004":4,"G_SYS_SECADV_005":4,"G_SYS_SECADV_006":4,"G_SYS_SECADV_009":4,"G_SYS_SECADV_010":4,"G_SYS_SECADV_011":4,"G_SYS_SECADV_012":4,"G_SYS_SECADV_014":4,"G_SYS_SECADV_015":4,"G_SYS_SECADV_016":4,"G_SYS_SECADV_018":4,"G_SYS_SECADV_019":4,"G_SYS_SECADV_020":4,"G_SYS_SECADV_021":4,"G_SYS_SECADV_023":4,"G_SYS_SECADV_025":4,"G_SYS_SECADV_026":4,"G_SYS_SECADV_028":4,"G_SYS_SECADV_029":4,"G_SYS_SECADV_038":4,"G_SYS_SECADV_042":4,"G_SYS_SECADV_043":4,"G_SYS_SECADV_044":4,"G_SYS_SECADV_046":4,"G_SYS_SECADV_049":4,"G_SYS_SECADV_050":4,"G_SYS_SECADV_052":4,"G_SYS_SECADV_053":4,"G_SYS_SECADV_055":4,"G_SYS_SECADV_057":4,"G_SYS_SECADV_058":4,"G_SYS_SECADV_059":4,"G_SYS_SECADV_060":4,"G_SYS_SECADV_061":4,"G_SYS_TRANS":3,"G_SYS_TRANS_001":4,"G_SYS_TRANS_002":4,"G_SYS_TRANS_003":4,"G_SYS_TRANS_004":4,"G_SYS_TRANS_006":4,"G_SYS_TRANS_009":4,"G_SYS_TRANS_010":4,"G_SYS_TRANS_012":4,"G_SYS_TRANS_015":4,"G_SYS_TRANS_016":4,"G_SYS_TRANS_017":4,"G_SYS_TRANS_018":4,"G_SYS_TRANS_021":4,"G_SYS_TRANS_022":4,"G_SYS_TRANS_023":4,"G_SYS_TRANS_024":4,"G_SOC_GOV_047":4,"A_INT_CASCADE":3,"A_INT_CASCADE_001":4,"A_INT_CASCADE_005":4,"A_INT_CASCADE_006":4,"A_INT_CASCADE_007":4,"A_INT_CASCADE_008":4,"A_INT_COLLUSION":3,"A_INT_COLLUSION_001":4,"A_INT_COLLUSION_002":4,"A_INT_COLLUSION_003":4,"A_INT_CONFLICT":3,"A_INT_CONFLICT_001":4,"A_INT_CONFLICT_002":4,"A_INT_CONFLICT_003":4,"A_INT_COORD":3,"A_INT_COORD_001":4,"A_INT_COORD_002":4,"A_INT_COORD_003":4,"A_INT_COORD_004":4,"A_INT_COORD_005":4,"A_INT_OVERSIGHT":3,"A_INT_OVERSIGHT_001":4,"A_INT_OVERSIGHT_002":4,"A_SYS_AUTH":3,"A_SYS_AUTH_001":4,"A_SYS_AUTH_002":4,"A_SYS_AUTH_003":4,"A_SYS_AUTH_005":4,"A_SYS_GOAL":3,"A_SYS_GOAL_024":4,"A_SYS_AUTH_009":4,"A_SYS_AUTH_010":4,"A_SYS_AUTH_012":4,"A_SYS_GOAL_025":4,"A_SYS_AUTH_017":4,"A_SYS_GOAL_026":4,"A_SYS_AUTH_024":4,"A_SYS_AUTH_025":4,"A_SYS_DECEPT":3,"A_SYS_DECEPT_001":4,"A_SYS_DECEPT_002":4,"A_SYS_DECEPT_003":4,"A_SYS_DECEPT_008":4,"A_SYS_DECEPT_009":4,"A_SYS_EXEC":3,"A_SYS_EXEC_002":4,"A_SYS_GOAL_003":4,"A_SYS_GOAL_005":4,"A_SYS_GOAL_006":4,"A_SYS_GOAL_007":4,"A_SYS_GOAL_009":4,"A_SYS_GOAL_011":4,"A_SYS_GOAL_012":4,"A_INT_OVERSIGHT_004":4,"A_SYS_GOAL_014":4,"A_SYS_GOAL_016":4,"A_SYS_GOAL_017":4,"A_SYS_GOAL_018":4,"A_SYS_GOAL_019":4,"A_INT_OVERSIGHT_005":4,"A_SYS_GOAL_022":4,"A_SYS_MEMSTATE":3,"A_SYS_MEMSTATE_001":4,"A_SYS_RESOURCE":3,"A_SYS_RESOURCE_001":4,"A_SYS_MEMSTATE_002":4,"A_SYS_SELFCOR":3,"A_SYS_SELFCOR_003":4,"A_SYS_TRACE":3,"A_SYS_TRACE_002":4,"A_SYS_TRACE_003":4,"P_INT_SAFETY":3,"P_INT_SAFETY_001":4,"P_INT_SAFETY_002":4,"P_INT_SAFETY_003":4,"P_INT_SAFETY_004":4,"P_INT_SAFETY_005":4,"P_INT_SAFETY_006":4,"P_INT_SAFETY_007":4,"P_INT_SAFETY_008":4,"P_INT_SAFETY_009":4,"P_INT_TAMPER":3,"P_INT_TAMPER_001":4,"P_INT_TAMPER_002":4,"P_INT_TAMPER_003":4,"P_INT_TAMPER_004":4,"P_SYS_CONTROL":3,"P_SYS_CONTROL_001":4,"P_SYS_CONTROL_002":4,"P_SYS_CONTROL_003":4,"P_SYS_CONTROL_004":4,"P_SYS_CONTROL_005":4,"P_SYS_CONTROL_006":4,"P_SYS_CONTROL_007":4,"P_SYS_CONTROL_008":4,"P_SYS_CONTROL_009":4,"P_SYS_CONTROL_010":4,"P_SYS_CONTROL_011":4,"P_SYS_HARDWARE":3,"P_SYS_HARDWARE_001":4,"P_SYS_HARDWARE_002":4,"P_SYS_HARDWARE_003":4,"P_SYS_HARDWARE_004":4,"P_SYS_PERCEPTION":3,"P_SYS_PERCEPTION_001":4,"P_SYS_PERCEPTION_002":4,"P_SYS_PERCEPTION_003":4,"P_SYS_PERCEPTION_004":4,"P_SYS_PERCEPTION_005":4,"P_SYS_PERCEPTION_006":4,"P_SYS_PERCEPTION_007":4,"P_SYS_PERCEPTION_008":4,"P_SYS_REALWORLD":3,"P_SYS_REALWORLD_001":4,"P_SYS_REALWORLD_002":4,"P_SYS_SAFESTATE":3,"P_SYS_SAFESTATE_001":4,"P_SYS_SAFESTATE_002":4,"P_SYS_SAFESTATE_003":4,"P_SYS_SAFESTATE_004":4,"P_SYS_SAFESTATE_005":4,"P_SYS_SAFESTATE_006":4,"P_SYS_TASKPLAN":3,"P_SYS_TASKPLAN_001":4,"P_SYS_TASKPLAN_002":4,"P_SYS_TASKPLAN_003":4,"P_SYS_TASKPLAN_004":4,"P_SYS_TASKPLAN_005":4,"P_SYS_TASKPLAN_006":4,"P_SYS_TIMESYNC":3,"P_SYS_TIMESYNC_001":4,"P_SYS_TIMESYNC_002":4,"P_SYS_TIMESYNC_003":4};
// The generated deployment includes HEART_COMMENT_RISK_IDS from risk-ids.json.
function heartCommentResponse(data, status, origin, env) {
  return new Response(status === 204 ? null : JSON.stringify(data), { status, headers: {
    'content-type': 'application/json; charset=utf-8',
    'access-control-allow-origin': origin === env.ALLOWED_ORIGIN ? origin : env.ALLOWED_ORIGIN,
    'access-control-allow-methods': 'GET, POST, OPTIONS',
    'access-control-allow-headers': 'content-type',
    'cache-control': 'no-store', vary: 'Origin',
  } });
}

async function heartCommentHash(secret) {
  const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(secret));
  return Array.from(new Uint8Array(bytes), value => value.toString(16).padStart(2, '0')).join('');
}

function heartPublicComment(row) {
  return { id: row.id, risk_id: row.risk_id, body: row.body, created_at: row.created_at, updated_at: row.updated_at };
}

function heartCommentHeaders(env) {
  return { authorization: `Bearer ${env.GH_TOKEN}`, accept: 'application/vnd.github+json',
    'content-type': 'application/json', 'user-agent': 'heart-anonymous-comments',
    'x-github-api-version': '2022-11-28' };
}

async function heartCommentDocument(riskId, env) {
  const path = `heart-comments/risks/${riskId}.json`;
  const endpoint = `https://api.github.com/repos/${env.GH_OWNER}/${env.GH_REPO}/contents/${path}`;
  const result = await fetch(endpoint, { headers: heartCommentHeaders(env), cache: 'no-store' });
  if (result.status === 404) return { endpoint, sha: null, comments: [] };
  if (!result.ok) throw new Error(`Comment store read ${result.status}`);
  const file = await result.json();
  const bytes = Uint8Array.from(atob(file.content.replace(/\s/g, '')), char => char.charCodeAt(0));
  const document = JSON.parse(new TextDecoder().decode(bytes));
  if (document.risk_id !== riskId || !Array.isArray(document.comments)) throw new Error('Invalid stored thread');
  return { endpoint, sha: file.sha, comments: document.comments };
}

async function heartCommentsFetch(request, env) {
  const origin = request.headers.get('origin') || '';
  const respond = (data, status = 200) => heartCommentResponse(data, status, origin, env);
  const url = new URL(request.url);
  if (request.method === 'OPTIONS') return respond(null, 204);
  const riskId = url.pathname.slice('/comments/'.length);
  if (!Object.hasOwn(HEART_COMMENT_RISK_IDS, riskId)) return respond({ error: 'Unknown risk ID' }, 404);
  if (!['GET', 'POST'].includes(request.method)) return respond({ error: 'Method not allowed' }, 405);
  if (request.method === 'POST' && origin !== env.ALLOWED_ORIGIN) return respond({ error: 'Origin not allowed' }, 403);
  try {
    if (request.method === 'GET') {
      const document = await heartCommentDocument(riskId, env);
      const offset = Math.max(0, Math.min(100000, Number.parseInt(url.searchParams.get('offset') || '0', 10) || 0));
      const rows = [...document.comments].sort((a, b) => b.created_at.localeCompare(a.created_at) || b.id.localeCompare(a.id));
      return respond({ comments: rows.slice(offset, offset + 30).map(heartPublicComment) });
    }
    if (!request.headers.get('content-type')?.startsWith('application/json')) return respond({ error: 'JSON required' }, 400);
    if (Number(request.headers.get('content-length')) > 16000) return respond({ error: 'Request too large' }, 413);
    const text = await request.text();
    if (new TextEncoder().encode(text).length > 16000) return respond({ error: 'Request too large' }, 413);
    let input;
    try { input = JSON.parse(text); } catch { return respond({ error: 'Invalid JSON' }, 400); }
    if (!/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i.test(input.id || '')
        || !/^[a-f0-9]{64}$/.test(input.edit_key || '') || typeof input.body !== 'string') {
      return respond({ error: 'Invalid comment' }, 400);
    }
    const body = input.body.trim();
    if (!body || Array.from(body).length > 2000) return respond({ error: 'Comment must contain 1 to 2000 characters' }, 400);
    const hash = await heartCommentHash(input.edit_key);
    for (let attempt = 0; attempt < 6; attempt++) {
      const document = await heartCommentDocument(riskId, env);
      const index = document.comments.findIndex(row => row.id === input.id);
      if (index >= 0 && document.comments[index].edit_hash !== hash) return respond({ error: 'Not the author' }, 403);
      if (index >= 0 && document.comments[index].body === body) return respond({ comment: heartPublicComment(document.comments[index]) });
      const now = new Date().toISOString();
      const row = { id: input.id, risk_id: riskId, body, edit_hash: hash,
        created_at: index >= 0 ? document.comments[index].created_at : now, updated_at: now };
      const comments = [...document.comments];
      if (index >= 0) comments[index] = row; else comments.push(row);
      const content = JSON.stringify({ schema_version: 1, risk_id: riskId, comments }, null, 2) + '\n';
      if (new TextEncoder().encode(content).length > 900000) return respond({ error: 'Thread capacity reached' }, 409);
      const result = await fetch(document.endpoint, { method: 'PUT', headers: heartCommentHeaders(env), body: JSON.stringify({
        message: `${index >= 0 ? 'Update' : 'Add'} anonymous HEART comment ${riskId}`,
        content: btoa(unescape(encodeURIComponent(content))), ...(document.sha ? { sha: document.sha } : {}),
      }) });
      if (result.ok) return respond({ comment: heartPublicComment(row) }, index >= 0 ? 200 : 201);
      if (![409, 422].includes(result.status)) throw new Error(`Comment store write ${result.status}`);
      await new Promise(resolve => setTimeout(resolve, 75 * (attempt + 1) + Math.random() * 100));
    }
    return respond({ error: 'Concurrent save, please retry' }, 409);
  } catch {
    return respond({ error: 'Comment store unavailable' }, 503);
  }
}

var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// src/index.js
var JSON_HEADERS = { "content-type": "application/json; charset=utf-8" };
function cors(origin, allowedOrigin) {
  const accepted = origin === allowedOrigin || origin === "http://127.0.0.1:8765";
  return {
    "access-control-allow-origin": accepted ? origin : allowedOrigin,
    "access-control-allow-methods": "POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-max-age": "86400",
    vary: "Origin"
  };
}
__name(cors, "cors");
function response(body, status, origin, env) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...JSON_HEADERS, ...cors(origin, env.ALLOWED_ORIGIN) }
  });
}
__name(response, "response");
function validPayload(payload) {
  return payload && /^R-[a-f0-9]{12}$/.test(payload.respondent_id || "") && /^A(?:0[1-9]|1[0-9])$/.test(payload.assignment_block || "") && /^[a-f0-9-]{36}$/.test(payload.submission_id || "") && typeof payload.markdown === "string" && payload.markdown.length >= 500 && payload.markdown.length <= 2e5 && typeof payload.json === "string" && payload.json.length >= 500 && payload.json.length <= 3e5 && typeof payload.csv === "string" && payload.csv.length >= 500 && payload.csv.length <= 3e5;
}
__name(validPayload, "validPayload");
function partition(dateValue) {
  const date = new Date(dateValue || Date.now());
  if (Number.isNaN(date.getTime())) throw new Error("Invalid timestamp");
  return {
    year: String(date.getUTCFullYear()),
    month: String(date.getUTCMonth() + 1).padStart(2, "0")
  };
}
__name(partition, "partition");
async function putGitHubFile(repo, path, content, message, env) {
  const endpoint = `https://api.github.com/repos/${env.GH_OWNER}/${repo}/contents/${path}`;
  const githubResponse = await fetch(endpoint, {
    method: "PUT",
    headers: {
      authorization: `Bearer ${env.GH_TOKEN}`,
      accept: "application/vnd.github+json",
      "content-type": "application/json",
      "user-agent": "pai-risk-survey-worker",
      "x-github-api-version": "2022-11-28"
    },
    body: JSON.stringify({
      message,
      content: btoa(unescape(encodeURIComponent(content)))
    })
  });
  if (githubResponse.status === 422) return { duplicate: true };
  if (!githubResponse.ok) {
    const detail = await githubResponse.text();
    throw new Error(`GitHub ${githubResponse.status}: ${detail.slice(0, 300)}`);
  }
  return { duplicate: false, result: await githubResponse.json() };
}
__name(putGitHubFile, "putGitHubFile");
function yamlValue(value) {
  return JSON.stringify(value ?? null);
}
__name(yamlValue, "yamlValue");
function buildTelemetry(payload, request, receivedAt) {
  const cf = request.cf || {};
  const startedAt = new Date(payload.started_at || receivedAt);
  const completedAt = new Date(payload.submitted_at || receivedAt);
  const durationSeconds = Number.isFinite(payload.duration_seconds) ? Math.max(0, Math.round(payload.duration_seconds)) : Math.max(0, Math.round((completedAt - startedAt) / 1e3));
  const telemetry = {
    respondent_id: payload.respondent_id,
    submission_id: payload.submission_id,
    assignment_block: payload.assignment_block,
    started_at_client: payload.started_at || null,
    completed_at_client: payload.submitted_at || null,
    duration_seconds: durationSeconds,
    country: cf.country || null
  };
  const lines = ["---"];
  for (const [key, value] of Object.entries(telemetry)) {
    lines.push(`${key}: ${yamlValue(value)}`);
  }
  lines.push("---", "", "# Private Survey Administration Record", "");
  lines.push("This file contains access-restricted timing and country-level information separated from the public survey response.", "");
  return lines.join("\n");
}
__name(buildTelemetry, "buildTelemetry");
async function saveTelemetry(payload, request, receivedAt, env) {
  const { year, month } = partition(receivedAt);
  const filename = `${payload.respondent_id}_${payload.submission_id}.md`;
  const path = `telemetry/${year}/${month}/${filename}`;
  const content = buildTelemetry(payload, request, receivedAt);
  const stored = await putGitHubFile(
    env.GH_TELEMETRY_REPO,
    path,
    content,
    `Add private survey telemetry ${payload.respondent_id}`,
    env
  );
  return { path, duplicate: stored.duplicate };
}
__name(saveTelemetry, "saveTelemetry");
async function savePublicResponse(payload, env) {
  const { year, month } = partition(payload.submitted_at);
  const stem = `${payload.respondent_id}_${payload.submission_id}`;
  const path = `responses/${year}/${month}/${stem}.md`;
  const jsonPath = `responses/${year}/${month}/${stem}.json`;
  const csvPath = `responses/${year}/${month}/${stem}.csv`;
  const markdown = await putGitHubFile(
    env.GH_REPO,
    path,
    payload.markdown,
    `Add anonymous survey response ${payload.respondent_id}`,
    env
  );
  const json = await putGitHubFile(
    env.GH_REPO,
    jsonPath,
    payload.json,
    `Add anonymous survey JSON ${payload.respondent_id}`,
    env
  );
  const csv = await putGitHubFile(
    env.GH_REPO,
    csvPath,
    payload.csv,
    `Add anonymous survey CSV ${payload.respondent_id}`,
    env
  );
  return {
    path,
    json_path: jsonPath,
    csv_path: csvPath,
    url: `https://github.com/${env.GH_OWNER}/${env.GH_REPO}/blob/main/${path}`,
    json_url: `https://github.com/${env.GH_OWNER}/${env.GH_REPO}/blob/main/${jsonPath}`,
    csv_url: `https://github.com/${env.GH_OWNER}/${env.GH_REPO}/blob/main/${csvPath}`,
    duplicate: markdown.duplicate && json.duplicate && csv.duplicate
  };
}
__name(savePublicResponse, "savePublicResponse");
var index_default = {
  async fetch(request, env) {
    if (new URL(request.url).pathname.startsWith('/comments/')) return heartCommentsFetch(request, env);
    const origin = request.headers.get("origin") || "";
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors(origin, env.ALLOWED_ORIGIN) });
    }
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/health") {
      return response({
        status: "ok",
        public_repository: `${env.GH_OWNER}/${env.GH_REPO}`,
        private_telemetry_repository: `${env.GH_OWNER}/${env.GH_TELEMETRY_REPO}`
      }, 200, origin, env);
    }
    if (request.method !== "POST" || url.pathname !== "/submit") {
      return response({ error: "Not found" }, 404, origin, env);
    }
    if (origin !== env.ALLOWED_ORIGIN && origin !== "http://127.0.0.1:8765") {
      return response({ error: "Origin not allowed" }, 403, origin, env);
    }
    let payload;
    try {
      payload = await request.json();
    } catch {
      return response({ error: "Invalid JSON" }, 400, origin, env);
    }
    if (!validPayload(payload)) return response({ error: "Invalid submission" }, 400, origin, env);
    try {
      const receivedAt = (/* @__PURE__ */ new Date()).toISOString();
      const telemetry = await saveTelemetry(payload, request, receivedAt, env);
      const publicResponse = await savePublicResponse(payload, env);
      return response({
        stored: true,
        ...publicResponse,
        telemetry_stored: true,
        telemetry_duplicate: telemetry.duplicate
      }, 201, origin, env);
    } catch (error) {
      console.error(error);
      return response({ error: "Storage failed" }, 502, origin, env);
    }
  }
};
export {
  index_default as default
};
//# sourceMappingURL=index.js.map
