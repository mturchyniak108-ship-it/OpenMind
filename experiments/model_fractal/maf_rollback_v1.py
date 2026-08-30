#!/usr/bin/env python3

"""Operational MAF rollback V1.

Rollback V1 reactivates retained immutable generation evidence.

It does not create or infer historical-authority provenance.
It does not own authority persistence.
"""

import maf_activation_v1_1 as activation


MAFRollbackError = activation.MAFActivationError
RollbackResult = activation.ActivationResult


def rollback_generation(
    *,
    model_pk,
    target_generation_pk,
    target_candidate_manifest_path,
    active_record_path,
    target_segment_paths,
):
    """Reactivate one retained generation for an already-active model."""

    current = activation.reopen_active_generation(
        active_record_path
    )

    if current["model_pk"] != model_pk:
        raise MAFRollbackError(
            "active model_pk mismatch"
        )

    return activation.activate_generation(
        model_pk=model_pk,
        generation_pk=target_generation_pk,
        candidate_manifest_path=(
            target_candidate_manifest_path
        ),
        active_record_path=active_record_path,
        segment_paths=target_segment_paths,
    )
