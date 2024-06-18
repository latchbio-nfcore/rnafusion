
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'skip_qc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Skip steps',
        description='Skip QC steps',
    ),
    'skip_vis': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip visualisation steps',
    ),
    'input': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'build_references': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specifies which analysis type for the pipeline - either build references or analyse data',
    ),
    'cosmic_username': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='COSMIC username',
    ),
    'cosmic_passwd': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='COSMIC password',
    ),
    'genomes_base': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Path to reference folder',
    ),
    'ensembl_version': NextflowParameter(
        type=typing.Optional[int],
        default=102,
        section_title=None,
        description='ensembl version',
    ),
    'starfusion_build': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='If set, starfusion references are built from scratch instead of downloaded (default)',
    ),
    'read_length': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Read length',
    ),
    'all': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build or run all references/analyses',
    ),
    'arriba': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build or run arriba references/analyses',
    ),
    'arriba_ref': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to arriba references',
    ),
    'arriba_ref_blacklist': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to arriba reference blacklist',
    ),
    'arriba_ref_cytobands': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to arriba reference cytobands',
    ),
    'arriba_ref_known_fusions': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to arriba reference known fusions',
    ),
    'arriba_ref_protein_domains': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to arriba reference protein domain',
    ),
    'arriba_fusions': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to arriba output',
    ),
    'ensembl_ref': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to ensembl references',
    ),
    'fusioncatcher': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build or run fusioncatcher references/analyses',
    ),
    'fusioncatcher_fusions': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to fusioncatcher output',
    ),
    'fusioncatcher_limitSjdbInsertNsj': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Use limitSjdbInsertNsj with int for fusioncatcher',
    ),
    'fusioncatcher_ref': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to fusioncatcher references',
    ),
    'fusioninspector_limitSjdbInsertNsj': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Use limitSjdbInsertNsj with int for fusioninspector STAR process',
    ),
    'fusioninspector_only': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip fusion-report. --fusioninspector_fusions PATH needed to provide a fusion list as input',
    ),
    'fusioninspector_fusions': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to a fusion list file built with format GENE1--GENE2',
    ),
    'fusionreport': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build fusionreport references',
    ),
    'fusionreport_ref': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to fusionreport references',
    ),
    'hgnc_ref': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to HGNC database file',
    ),
    'hgnc_date': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to HGNC timestamp file for database retrieval',
    ),
    'qiagen': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Use QIAGEN instead of SANGER to download COSMIC database',
    ),
    'starfusion': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build or run starfusion references/analyses',
    ),
    'starfusion_fusions': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to starfusion output',
    ),
    'starfusion_ref': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to starfusion references',
    ),
    'starindex': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Build or run starindex references/analyses',
    ),
    'starindex_ref': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to starindex references',
    ),
    'stringtie': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Run stringtie analysis',
    ),
    'tools_cutoff': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Discard fusions identified by less than INT tools',
    ),
    'whitelist': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to fusions to add to the input of fusioninspector',
    ),
    'fastp_trim': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Read trimming options',
        description='Preform fastp trimming of reads, default: false',
    ),
    'trim_tail': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Preform tail trimming of reads, default: null',
    ),
    'adapter_fasta': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to adapter fasta file: default: []',
    ),
    'cram': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Alignment compression options',
        description='List of tools for which to compress BAM file to CRAM,default: [], options: arriba, starfusion. Leave no space between options',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'fai': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome index file.',
    ),
    'gtf': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to GTF genome file.',
    ),
    'chrgtf': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to GTF genome file.',
    ),
    'transcript': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to GTF genome file.',
    ),
    'refflat': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to GTF genome file.',
    ),
    'rrna_intervals': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to ribosomal interval list.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

