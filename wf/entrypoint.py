import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Annotated, List, Optional

import requests
import typing_extensions
from flytekit.core.annotation import FlyteAnnotation
from latch.executions import rename_current_execution, report_nextflow_used_storage
from latch.ldata.path import LPath
from latch.resources.tasks import custom_task, nextflow_runtime_task
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.nextflow.workflow import get_flag
from latch_cli.services.register.utils import import_module_by_path
from latch_cli.utils import urljoins

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

sys.stdout.reconfigure(line_buffering=True)


@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_expiration_hours": 0,
            "version": 2,
        },
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]


@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(
    run_name: Annotated[
        str,
        FlyteAnnotation(
            {
                "rules": [
                    {
                        "regex": r"^[a-zA-Z0-9_-]+$",
                        "message": "ID name must contain only letters, digits, underscores, and dashes. No spaces are allowed.",
                    }
                ],
            }
        ),
    ],
    pvc_name: str,
    skip_qc: bool,
    skip_vis: bool,
    input: Optional[LatchFile],
    outdir: LatchOutputDir,
    email: Optional[str],
    multiqc_title: Optional[str],
    build_references: bool,
    cosmic_username: Optional[str],
    cosmic_passwd: Optional[str],
    genomes_base: str,
    starfusion_build: bool,
    all: bool,
    arriba: bool,
    arriba_ref: Optional[str],
    arriba_ref_blacklist: Optional[str],
    arriba_ref_cytobands: Optional[str],
    arriba_ref_known_fusions: Optional[str],
    arriba_ref_protein_domains: Optional[str],
    arriba_fusions: Optional[str],
    ensembl_ref: Optional[str],
    fusioncatcher: bool,
    fusioncatcher_fusions: Optional[str],
    fusioncatcher_limitSjdbInsertNsj: Optional[int],
    fusioncatcher_ref: Optional[str],
    fusioninspector_limitSjdbInsertNsj: Optional[int],
    fusioninspector_only: bool,
    fusioninspector_fusions: Optional[str],
    fusionreport: bool,
    fusionreport_ref: Optional[str],
    hgnc_ref: Optional[str],
    hgnc_date: Optional[str],
    qiagen: bool,
    starfusion: bool,
    starfusion_fusions: Optional[str],
    starfusion_ref: Optional[str],
    starindex: bool,
    starindex_ref: Optional[str],
    stringtie: bool,
    tools_cutoff: Optional[int],
    whitelist: Optional[str],
    fastp_trim: bool,
    trim_tail: Optional[int],
    adapter_fasta: Optional[str],
    cram: Optional[str],
    genome: Optional[str],
    fasta: Optional[LatchFile],
    fai: Optional[LatchFile],
    gtf: Optional[LatchFile],
    chrgtf: Optional[LatchFile],
    transcript: Optional[LatchFile],
    refflat: Optional[LatchFile],
    rrna_intervals: Optional[LatchFile],
    multiqc_methods_description: Optional[str],
    ensembl_version: Optional[int],
    read_length: Optional[int],
) -> None:
    shared_dir = Path("/nf-workdir")
    rename_current_execution(str(run_name))

    ignore_list = [
        "latch",
        ".latch",
        ".git",
        "nextflow",
        ".nextflow",
        "work",
        "results",
        "miniconda",
        "anaconda3",
        "mambaforge",
    ]

    shutil.copytree(
        Path("/root"),
        shared_dir,
        ignore=lambda src, names: ignore_list,
        ignore_dangling_symlinks=True,
        dirs_exist_ok=True,
    )

    profile_list = ["docker", "test"]

    if len(profile_list) == 0:
        profile_list.append("standard")

    profiles = ",".join(profile_list)

    cmd = [
        "/root/nextflow",
        "run",
        str(shared_dir / "main.nf"),
        "-work-dir",
        str(shared_dir),
        "-profile",
        profiles,
        "-c",
        "latch.config",
        "-resume",
        *get_flag("skip_qc", skip_qc),
        *get_flag("skip_vis", skip_vis),
        *get_flag("input", input),
        *get_flag("outdir", LatchOutputDir(f"{outdir.remote_path}/{run_name}")),
        *get_flag("email", email),
        *get_flag("multiqc_title", multiqc_title),
        *get_flag("build_references", build_references),
        *get_flag("cosmic_username", cosmic_username),
        *get_flag("cosmic_passwd", cosmic_passwd),
        *get_flag("genomes_base", genomes_base),
        *get_flag("ensembl_version", ensembl_version),
        *get_flag("starfusion_build", starfusion_build),
        *get_flag("read_length", read_length),
        *get_flag("all", all),
        *get_flag("arriba", arriba),
        *get_flag("arriba_ref", arriba_ref),
        *get_flag("arriba_ref_blacklist", arriba_ref_blacklist),
        *get_flag("arriba_ref_cytobands", arriba_ref_cytobands),
        *get_flag("arriba_ref_known_fusions", arriba_ref_known_fusions),
        *get_flag("arriba_ref_protein_domains", arriba_ref_protein_domains),
        *get_flag("arriba_fusions", arriba_fusions),
        *get_flag("ensembl_ref", ensembl_ref),
        *get_flag("fusioncatcher", fusioncatcher),
        *get_flag("fusioncatcher_fusions", fusioncatcher_fusions),
        *get_flag("fusioncatcher_limitSjdbInsertNsj", fusioncatcher_limitSjdbInsertNsj),
        *get_flag("fusioncatcher_ref", fusioncatcher_ref),
        *get_flag("fusioninspector_limitSjdbInsertNsj", fusioninspector_limitSjdbInsertNsj),
        *get_flag("fusioninspector_only", fusioninspector_only),
        *get_flag("fusioninspector_fusions", fusioninspector_fusions),
        *get_flag("fusionreport", fusionreport),
        *get_flag("fusionreport_ref", fusionreport_ref),
        *get_flag("hgnc_ref", hgnc_ref),
        *get_flag("hgnc_date", hgnc_date),
        *get_flag("qiagen", qiagen),
        *get_flag("starfusion", starfusion),
        *get_flag("starfusion_fusions", starfusion_fusions),
        *get_flag("starfusion_ref", starfusion_ref),
        *get_flag("starindex", starindex),
        *get_flag("starindex_ref", starindex_ref),
        *get_flag("stringtie", stringtie),
        *get_flag("tools_cutoff", tools_cutoff),
        *get_flag("whitelist", whitelist),
        *get_flag("fastp_trim", fastp_trim),
        *get_flag("trim_tail", trim_tail),
        *get_flag("adapter_fasta", adapter_fasta),
        *get_flag("cram", cram),
        *get_flag("genome", genome),
        *get_flag("fasta", fasta),
        *get_flag("fai", fai),
        *get_flag("gtf", gtf),
        *get_flag("chrgtf", chrgtf),
        *get_flag("transcript", transcript),
        *get_flag("refflat", refflat),
        *get_flag("rrna_intervals", rrna_intervals),
        *get_flag("multiqc_methods_description", multiqc_methods_description),
    ]

    print("Launching Nextflow Runtime")
    print(" ".join(cmd))
    print(flush=True)

    failed = False
    try:
        env = {
            **os.environ,
            "NXF_ANSI_LOG": "false",
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms1536M -Xmx6144M -XX:ActiveProcessorCount=4",
            "NXF_DISABLE_CHECK_LATEST": "true",
            "NXF_ENABLE_VIRTUAL_THREADS": "false",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    except subprocess.CalledProcessError:
        failed = True
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_rnafusion", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)

        print("Computing size of workdir... ", end="")
        try:
            result = subprocess.run(
                ["du", "-sb", str(shared_dir)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5 * 60,
            )

            size = int(result.stdout.split()[0])
            report_nextflow_used_storage(size)
            print(f"Done. Workdir size: {size / 1024 / 1024 / 1024: .2f} GiB")
        except subprocess.TimeoutExpired:
            print("Failed to compute storage size: Operation timed out after 5 minutes.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to compute storage size: {e.stderr}")
        except Exception as e:
            print(f"Failed to compute storage size: {e}")

    if failed:
        sys.exit(1)


@workflow(metadata._nextflow_metadata)
def nf_nf_core_rnafusion(
    run_name: Annotated[
        str,
        FlyteAnnotation(
            {
                "rules": [
                    {
                        "regex": r"^[a-zA-Z0-9_-]+$",
                        "message": "ID name must contain only letters, digits, underscores, and dashes. No spaces are allowed.",
                    }
                ],
            }
        ),
    ],
    skip_qc: bool,
    skip_vis: bool,
    input: Optional[LatchFile],
    outdir: LatchOutputDir,
    email: Optional[str],
    multiqc_title: Optional[str],
    build_references: bool,
    cosmic_username: Optional[str],
    cosmic_passwd: Optional[str],
    genomes_base: str,
    starfusion_build: bool,
    all: bool,
    arriba: bool,
    arriba_ref: Optional[str],
    arriba_ref_blacklist: Optional[str],
    arriba_ref_cytobands: Optional[str],
    arriba_ref_known_fusions: Optional[str],
    arriba_ref_protein_domains: Optional[str],
    arriba_fusions: Optional[str],
    ensembl_ref: Optional[str],
    fusioncatcher: bool,
    fusioncatcher_fusions: Optional[str],
    fusioncatcher_limitSjdbInsertNsj: Optional[int],
    fusioncatcher_ref: Optional[str],
    fusioninspector_limitSjdbInsertNsj: Optional[int],
    fusioninspector_only: bool,
    fusioninspector_fusions: Optional[str],
    fusionreport: bool,
    fusionreport_ref: Optional[str],
    hgnc_ref: Optional[str],
    hgnc_date: Optional[str],
    qiagen: bool,
    starfusion: bool,
    starfusion_fusions: Optional[str],
    starfusion_ref: Optional[str],
    starindex: bool,
    starindex_ref: Optional[str],
    stringtie: bool,
    tools_cutoff: Optional[int],
    whitelist: Optional[str],
    fastp_trim: bool,
    trim_tail: Optional[int],
    adapter_fasta: Optional[str],
    cram: Optional[str],
    genome: Optional[str],
    fasta: Optional[LatchFile],
    fai: Optional[LatchFile],
    gtf: Optional[LatchFile],
    chrgtf: Optional[LatchFile],
    transcript: Optional[LatchFile],
    refflat: Optional[LatchFile],
    rrna_intervals: Optional[LatchFile],
    multiqc_methods_description: Optional[str],
    ensembl_version: Optional[int] = 102,
    read_length: Optional[int] = 100,
) -> None:
    """
    nf-core/rnafusion

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(
        run_name=run_name,
        pvc_name=pvc_name,
        skip_qc=skip_qc,
        skip_vis=skip_vis,
        input=input,
        outdir=outdir,
        email=email,
        multiqc_title=multiqc_title,
        build_references=build_references,
        cosmic_username=cosmic_username,
        cosmic_passwd=cosmic_passwd,
        genomes_base=genomes_base,
        ensembl_version=ensembl_version,
        starfusion_build=starfusion_build,
        read_length=read_length,
        all=all,
        arriba=arriba,
        arriba_ref=arriba_ref,
        arriba_ref_blacklist=arriba_ref_blacklist,
        arriba_ref_cytobands=arriba_ref_cytobands,
        arriba_ref_known_fusions=arriba_ref_known_fusions,
        arriba_ref_protein_domains=arriba_ref_protein_domains,
        arriba_fusions=arriba_fusions,
        ensembl_ref=ensembl_ref,
        fusioncatcher=fusioncatcher,
        fusioncatcher_fusions=fusioncatcher_fusions,
        fusioncatcher_limitSjdbInsertNsj=fusioncatcher_limitSjdbInsertNsj,
        fusioncatcher_ref=fusioncatcher_ref,
        fusioninspector_limitSjdbInsertNsj=fusioninspector_limitSjdbInsertNsj,
        fusioninspector_only=fusioninspector_only,
        fusioninspector_fusions=fusioninspector_fusions,
        fusionreport=fusionreport,
        fusionreport_ref=fusionreport_ref,
        hgnc_ref=hgnc_ref,
        hgnc_date=hgnc_date,
        qiagen=qiagen,
        starfusion=starfusion,
        starfusion_fusions=starfusion_fusions,
        starfusion_ref=starfusion_ref,
        starindex=starindex,
        starindex_ref=starindex_ref,
        stringtie=stringtie,
        tools_cutoff=tools_cutoff,
        whitelist=whitelist,
        fastp_trim=fastp_trim,
        trim_tail=trim_tail,
        adapter_fasta=adapter_fasta,
        cram=cram,
        genome=genome,
        fasta=fasta,
        fai=fai,
        gtf=gtf,
        chrgtf=chrgtf,
        transcript=transcript,
        refflat=refflat,
        rrna_intervals=rrna_intervals,
        multiqc_methods_description=multiqc_methods_description,
    )
