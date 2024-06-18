from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

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
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, skip_qc: typing.Optional[bool], skip_vis: typing.Optional[bool], input: typing.Optional[LatchFile], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], build_references: typing.Optional[bool], cosmic_username: typing.Optional[str], cosmic_passwd: typing.Optional[str], genomes_base: str, starfusion_build: typing.Optional[bool], all: typing.Optional[bool], arriba: typing.Optional[bool], arriba_ref: typing.Optional[str], arriba_ref_blacklist: typing.Optional[str], arriba_ref_cytobands: typing.Optional[str], arriba_ref_known_fusions: typing.Optional[str], arriba_ref_protein_domains: typing.Optional[str], arriba_fusions: typing.Optional[str], ensembl_ref: typing.Optional[str], fusioncatcher: typing.Optional[bool], fusioncatcher_fusions: typing.Optional[str], fusioncatcher_limitSjdbInsertNsj: typing.Optional[int], fusioncatcher_ref: typing.Optional[str], fusioninspector_limitSjdbInsertNsj: typing.Optional[int], fusioninspector_only: typing.Optional[bool], fusioninspector_fusions: typing.Optional[str], fusionreport: typing.Optional[bool], fusionreport_ref: typing.Optional[str], hgnc_ref: typing.Optional[str], hgnc_date: typing.Optional[str], qiagen: typing.Optional[bool], starfusion: typing.Optional[bool], starfusion_fusions: typing.Optional[str], starfusion_ref: typing.Optional[str], starindex: typing.Optional[bool], starindex_ref: typing.Optional[str], stringtie: typing.Optional[bool], tools_cutoff: typing.Optional[int], whitelist: typing.Optional[str], fastp_trim: typing.Optional[bool], trim_tail: typing.Optional[int], adapter_fasta: typing.Optional[str], cram: typing.Optional[str], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], fai: typing.Optional[LatchFile], gtf: typing.Optional[LatchFile], chrgtf: typing.Optional[LatchFile], transcript: typing.Optional[LatchFile], refflat: typing.Optional[LatchFile], rrna_intervals: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], ensembl_version: typing.Optional[int], read_length: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
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

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('skip_qc', skip_qc),
                *get_flag('skip_vis', skip_vis),
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('build_references', build_references),
                *get_flag('cosmic_username', cosmic_username),
                *get_flag('cosmic_passwd', cosmic_passwd),
                *get_flag('genomes_base', genomes_base),
                *get_flag('ensembl_version', ensembl_version),
                *get_flag('starfusion_build', starfusion_build),
                *get_flag('read_length', read_length),
                *get_flag('all', all),
                *get_flag('arriba', arriba),
                *get_flag('arriba_ref', arriba_ref),
                *get_flag('arriba_ref_blacklist', arriba_ref_blacklist),
                *get_flag('arriba_ref_cytobands', arriba_ref_cytobands),
                *get_flag('arriba_ref_known_fusions', arriba_ref_known_fusions),
                *get_flag('arriba_ref_protein_domains', arriba_ref_protein_domains),
                *get_flag('arriba_fusions', arriba_fusions),
                *get_flag('ensembl_ref', ensembl_ref),
                *get_flag('fusioncatcher', fusioncatcher),
                *get_flag('fusioncatcher_fusions', fusioncatcher_fusions),
                *get_flag('fusioncatcher_limitSjdbInsertNsj', fusioncatcher_limitSjdbInsertNsj),
                *get_flag('fusioncatcher_ref', fusioncatcher_ref),
                *get_flag('fusioninspector_limitSjdbInsertNsj', fusioninspector_limitSjdbInsertNsj),
                *get_flag('fusioninspector_only', fusioninspector_only),
                *get_flag('fusioninspector_fusions', fusioninspector_fusions),
                *get_flag('fusionreport', fusionreport),
                *get_flag('fusionreport_ref', fusionreport_ref),
                *get_flag('hgnc_ref', hgnc_ref),
                *get_flag('hgnc_date', hgnc_date),
                *get_flag('qiagen', qiagen),
                *get_flag('starfusion', starfusion),
                *get_flag('starfusion_fusions', starfusion_fusions),
                *get_flag('starfusion_ref', starfusion_ref),
                *get_flag('starindex', starindex),
                *get_flag('starindex_ref', starindex_ref),
                *get_flag('stringtie', stringtie),
                *get_flag('tools_cutoff', tools_cutoff),
                *get_flag('whitelist', whitelist),
                *get_flag('fastp_trim', fastp_trim),
                *get_flag('trim_tail', trim_tail),
                *get_flag('adapter_fasta', adapter_fasta),
                *get_flag('cram', cram),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('fai', fai),
                *get_flag('gtf', gtf),
                *get_flag('chrgtf', chrgtf),
                *get_flag('transcript', transcript),
                *get_flag('refflat', refflat),
                *get_flag('rrna_intervals', rrna_intervals),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
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



@workflow(metadata._nextflow_metadata)
def nf_nf_core_rnafusion(skip_qc: typing.Optional[bool], skip_vis: typing.Optional[bool], input: typing.Optional[LatchFile], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], build_references: typing.Optional[bool], cosmic_username: typing.Optional[str], cosmic_passwd: typing.Optional[str], genomes_base: str, starfusion_build: typing.Optional[bool], all: typing.Optional[bool], arriba: typing.Optional[bool], arriba_ref: typing.Optional[str], arriba_ref_blacklist: typing.Optional[str], arriba_ref_cytobands: typing.Optional[str], arriba_ref_known_fusions: typing.Optional[str], arriba_ref_protein_domains: typing.Optional[str], arriba_fusions: typing.Optional[str], ensembl_ref: typing.Optional[str], fusioncatcher: typing.Optional[bool], fusioncatcher_fusions: typing.Optional[str], fusioncatcher_limitSjdbInsertNsj: typing.Optional[int], fusioncatcher_ref: typing.Optional[str], fusioninspector_limitSjdbInsertNsj: typing.Optional[int], fusioninspector_only: typing.Optional[bool], fusioninspector_fusions: typing.Optional[str], fusionreport: typing.Optional[bool], fusionreport_ref: typing.Optional[str], hgnc_ref: typing.Optional[str], hgnc_date: typing.Optional[str], qiagen: typing.Optional[bool], starfusion: typing.Optional[bool], starfusion_fusions: typing.Optional[str], starfusion_ref: typing.Optional[str], starindex: typing.Optional[bool], starindex_ref: typing.Optional[str], stringtie: typing.Optional[bool], tools_cutoff: typing.Optional[int], whitelist: typing.Optional[str], fastp_trim: typing.Optional[bool], trim_tail: typing.Optional[int], adapter_fasta: typing.Optional[str], cram: typing.Optional[str], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], fai: typing.Optional[LatchFile], gtf: typing.Optional[LatchFile], chrgtf: typing.Optional[LatchFile], transcript: typing.Optional[LatchFile], refflat: typing.Optional[LatchFile], rrna_intervals: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], ensembl_version: typing.Optional[int] = 102, read_length: typing.Optional[int] = 100) -> None:
    """
    nf-core/rnafusion

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, skip_qc=skip_qc, skip_vis=skip_vis, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, build_references=build_references, cosmic_username=cosmic_username, cosmic_passwd=cosmic_passwd, genomes_base=genomes_base, ensembl_version=ensembl_version, starfusion_build=starfusion_build, read_length=read_length, all=all, arriba=arriba, arriba_ref=arriba_ref, arriba_ref_blacklist=arriba_ref_blacklist, arriba_ref_cytobands=arriba_ref_cytobands, arriba_ref_known_fusions=arriba_ref_known_fusions, arriba_ref_protein_domains=arriba_ref_protein_domains, arriba_fusions=arriba_fusions, ensembl_ref=ensembl_ref, fusioncatcher=fusioncatcher, fusioncatcher_fusions=fusioncatcher_fusions, fusioncatcher_limitSjdbInsertNsj=fusioncatcher_limitSjdbInsertNsj, fusioncatcher_ref=fusioncatcher_ref, fusioninspector_limitSjdbInsertNsj=fusioninspector_limitSjdbInsertNsj, fusioninspector_only=fusioninspector_only, fusioninspector_fusions=fusioninspector_fusions, fusionreport=fusionreport, fusionreport_ref=fusionreport_ref, hgnc_ref=hgnc_ref, hgnc_date=hgnc_date, qiagen=qiagen, starfusion=starfusion, starfusion_fusions=starfusion_fusions, starfusion_ref=starfusion_ref, starindex=starindex, starindex_ref=starindex_ref, stringtie=stringtie, tools_cutoff=tools_cutoff, whitelist=whitelist, fastp_trim=fastp_trim, trim_tail=trim_tail, adapter_fasta=adapter_fasta, cram=cram, genome=genome, fasta=fasta, fai=fai, gtf=gtf, chrgtf=chrgtf, transcript=transcript, refflat=refflat, rrna_intervals=rrna_intervals, multiqc_methods_description=multiqc_methods_description)

