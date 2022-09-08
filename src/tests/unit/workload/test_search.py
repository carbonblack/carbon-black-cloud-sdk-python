#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2021-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Unit test code for ComputeResource"""

import pytest
import logging
from cbc_sdk.errors import ApiError
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from cbc_sdk.workload.vm_workloads_search import ComputeResource, AWSComputeResource
from tests.unit.fixtures.workload.mock_search import (FETCH_COMPUTE_RESOURCE_BY_ID_RESP, FETCH_AWS_RESOURCE_BY_ID_RESP,
                                                      SEARCH_COMPUTE_RESOURCES, SEARCH_AWS_RESOURCES)


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(url="https://example.com",
                      org_key="test",
                      token="abcd/1234",
                      ssl_verify=False)


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================

def test_compute_resource_by_id(cbcsdk_mock):
    """Tests a simple compute resource query"""
    cbcsdk_mock.mock_request("GET", "/lcm/view/v2/orgs/test/compute_resources/15396109?deployment_type=WORKLOAD",
                             FETCH_COMPUTE_RESOURCE_BY_ID_RESP)
    api = cbcsdk_mock.api
    resource = ComputeResource(api, "15396109")
    assert resource._model_unique_id == "15396109"


def test_aws_resource_by_id(cbcsdk_mock):
    """Tests an AWS compute resource query."""
    cbcsdk_mock.mock_request("GET", "/lcm/view/v2/orgs/test/compute_resources/7001?deployment_type=AWS",
                             FETCH_AWS_RESOURCE_BY_ID_RESP)
    api = cbcsdk_mock.api
    resource = AWSComputeResource(api, "7001")
    assert resource._model_unique_id == "7001"


def test_search_resource_async(cbcsdk_mock):
    """Tests running the async_query."""
    def post_validate(url, body, **kwargs):
        crits = body['criteria']
        assert crits['deployment_type'] == ['WORKLOAD']
        assert crits['uuid'] == ['502277cc-0aa9-80b0-9ac8-6f540c11edaf']
        assert body['sort'] == [{"field": "name", "order": "ASC"}]

        return SEARCH_COMPUTE_RESOURCES

    cbcsdk_mock.mock_request("POST", "/lcm/view/v2/orgs/test/compute_resources/_search",
                             post_validate)
    api = cbcsdk_mock.api
    query = api.select(ComputeResource).set_uuid(['502277cc-0aa9-80b0-9ac8-6f540c11edaf']).sort_by("name", "ASC")

    assert query._count() == 1
    results = [result for result in query._run_async_query(None)]
    assert len(results) == 1
    resource = results[0]
    assert resource.uuid == '502277cc-0aa9-80b0-9ac8-6f540c11edaf'


def test_search_resource_with_all_bells_and_whistles(cbcsdk_mock):
    """Tests running the query with all values set."""
    def post_validate(url, body, **kwargs):
        crits = body['criteria']
        assert crits['deployment_type'] == ['WORKLOAD']
        assert crits['appliance_uuid'] == ['c89f183b-f201-4bca-bacc-80184b5b8823']
        assert crits['cluster_name'] == ['launcher-cluster']
        assert crits['datacenter_name'] == ['launcher-dc']
        assert crits['esx_host_name'] == ['10.105.5.70']
        assert crits['esx_host_uuid'] == ['d5304d56-5004-a871-1ad1-bd4b4af9977d']
        assert crits['vcenter_name'] == ['VMware vCenter Server 7.0.0 build-15952599']
        assert crits['vcenter_host_url'] == ['10.105.5.63']
        assert crits['vcenter_uuid'] == ['4a6b1382-f917-4e1a-8564-374cb7274bd7']
        assert crits['name'] == ['vsvv-2k8r2']
        assert crits['host_name'] == ['QUIMBY']
        assert crits['ip_address'] == ['192.168.1.1']
        assert crits['device_guid'] == ['a12e0d99-2114-459c-abf8-1af5f719f121']
        assert crits['registration_id'] == ['20-112233999']
        assert crits['eligibility'] == ['NOT_ELIGIBLE']
        assert crits['eligibility_code'] == ['VM is offline']
        assert crits['installation_status'] == ['NOT_INSTALLED']
        assert crits['installation_type'] == ['A']
        assert crits['uuid'] == ['502277cc-0aa9-80b0-9ac8-6f540c11edaf']
        assert crits['os_description'] == ['Windows 10 32-bit']
        assert crits['os_type'] == ['WINDOWS']
        assert crits['os_architecture'] == ['32']
        assert crits['vmwaretools_version'] == ["0"]

        excls = body['exclusions']
        assert excls['appliance_uuid'] == ['9ee441c2-f245-435d-82d5-615668b760f9']
        assert excls['cluster_name'] == ['notmy-cluster']
        assert excls['datacenter_name'] == ['notmy-dc']
        assert excls['esx_host_name'] == ['10.29.99.254']
        assert excls['esx_host_uuid'] == ['9fd12239-ce58-4b61-9560-ef4d3c1bb231']
        assert excls['vcenter_name'] == ['Not VMware']
        assert excls['vcenter_host_url'] == ['10.29.99.64']
        assert excls['vcenter_uuid'] == ['1bba86cd-4656-4810-92c1-0875bb8cbf1c']
        assert excls['name'] == ['vrmm-ou812']
        assert excls['host_name'] == ['NOTEXIST']
        assert excls['ip_address'] == ['192.168.42.42']
        assert excls['device_guid'] == ['ad1a6505-659c-46d3-8f3a-2e1363e2f782']
        assert excls['registration_id'] == ['666']
        assert excls['eligibility'] == ['ELIGIBLE']
        assert excls['eligibility_code'] == ['Bogus']
        assert excls['installation_status'] == ['SUCCESS']
        assert excls['installation_type'] == ['Z']
        assert excls['uuid'] == ['6fb6a53c-350f-4fda-a793-641ac8c7b188']
        assert excls['os_description'] == ['Linux']
        assert excls['os_type'] == ['RHEL']
        assert excls['os_architecture'] == ['64']
        assert excls['vmwaretools_version'] == ['105']

        return SEARCH_COMPUTE_RESOURCES

    cbcsdk_mock.mock_request("POST", "/lcm/view/v2/orgs/test/compute_resources/_search",
                             post_validate)
    api = cbcsdk_mock.api
    query = api.select(ComputeResource).set_appliance_uuid(['c89f183b-f201-4bca-bacc-80184b5b8823']) \
        .set_cluster_name(['launcher-cluster']).set_datacenter_name(['launcher-dc']) \
        .set_esx_host_name(['10.105.5.70']).set_esx_host_uuid(['d5304d56-5004-a871-1ad1-bd4b4af9977d']) \
        .set_vcenter_name(['VMware vCenter Server 7.0.0 build-15952599']).set_vcenter_host_url(['10.105.5.63']) \
        .set_vcenter_uuid(['4a6b1382-f917-4e1a-8564-374cb7274bd7']).set_name(['vsvv-2k8r2']) \
        .set_host_name(['QUIMBY']).set_ip_address(['192.168.1.1']) \
        .set_device_guid(['a12e0d99-2114-459c-abf8-1af5f719f121']).set_registration_id(['20-112233999']) \
        .set_eligibility(['NOT_ELIGIBLE']).set_eligibility_code(['VM is offline']) \
        .set_installation_status(['NOT_INSTALLED']).set_installation_type(['A']) \
        .set_uuid(['502277cc-0aa9-80b0-9ac8-6f540c11edaf']).set_os_description(['Windows 10 32-bit']) \
        .set_os_type(['WINDOWS']).set_os_architecture(['32']).set_vmwaretools_version(["0"]) \
        .exclude_appliance_uuid(['9ee441c2-f245-435d-82d5-615668b760f9']).exclude_cluster_name(['notmy-cluster']) \
        .exclude_datacenter_name(['notmy-dc']).exclude_esx_host_name(['10.29.99.254']) \
        .exclude_esx_host_uuid(['9fd12239-ce58-4b61-9560-ef4d3c1bb231']).exclude_vcenter_name(['Not VMware']) \
        .exclude_vcenter_host_url(['10.29.99.64']).exclude_vcenter_uuid(['1bba86cd-4656-4810-92c1-0875bb8cbf1c']) \
        .exclude_name(['vrmm-ou812']).exclude_host_name(['NOTEXIST']).exclude_ip_address(['192.168.42.42']) \
        .exclude_device_guid(['ad1a6505-659c-46d3-8f3a-2e1363e2f782']).exclude_registration_id(['666']) \
        .exclude_eligibility(['ELIGIBLE']).exclude_eligibility_code(['Bogus']) \
        .exclude_installation_status(['SUCCESS']).exclude_installation_type(['Z']) \
        .exclude_uuid(['6fb6a53c-350f-4fda-a793-641ac8c7b188']).exclude_os_description(['Linux']) \
        .exclude_os_type(['RHEL']).exclude_os_architecture(['64']).exclude_vmwaretools_version(['105'])

    assert query._count() == 1
    results = [result for result in query._perform_query()]
    assert len(results) == 1
    resource = results[0]
    assert resource.appliance_uuid == 'c89f183b-f201-4bca-bacc-80184b5b8823'
    assert resource.eligibility == 'NOT_ELIGIBLE'
    assert resource.cluster_name == 'launcher-cluster'
    assert resource.name == 'vsvv-2k8r2'
    assert resource.ip_address == '192.168.1.1'
    assert resource.installation_status == 'NOT_INSTALLED'
    assert resource.uuid == '502277cc-0aa9-80b0-9ac8-6f540c11edaf'
    assert resource.os_type == 'WINDOWS'
    assert resource.os_architecture == '32'


def test_search_resource_failures(cbcsdk_mock):
    """Testng all set methods for failure."""
    query = cbcsdk_mock.api.select(ComputeResource)
    with pytest.raises(ApiError):
        query.set_appliance_uuid([1])
    with pytest.raises(ApiError):
        query.set_cluster_name([1])
    with pytest.raises(ApiError):
        query.set_datacenter_name([1])
    with pytest.raises(ApiError):
        query.set_esx_host_name([1])
    with pytest.raises(ApiError):
        query.set_esx_host_uuid([1])
    with pytest.raises(ApiError):
        query.set_vcenter_name([1])
    with pytest.raises(ApiError):
        query.set_vcenter_host_url([1])
    with pytest.raises(ApiError):
        query.set_vcenter_uuid([1])
    with pytest.raises(ApiError):
        query.set_name([1])
    with pytest.raises(ApiError):
        query.set_host_name([1])
    with pytest.raises(ApiError):
        query.set_ip_address([1])
    with pytest.raises(ApiError):
        query.set_device_guid([1])
    with pytest.raises(ApiError):
        query.set_registration_id([1])
    with pytest.raises(ApiError):
        query.set_eligibility([1])
    with pytest.raises(ApiError):
        query.set_eligibility_code([1])
    with pytest.raises(ApiError):
        query.set_installation_status([1])
    with pytest.raises(ApiError):
        query.set_installation_type([1])
    with pytest.raises(ApiError):
        query.set_uuid([1])
    with pytest.raises(ApiError):
        query.set_os_description([1])
    with pytest.raises(ApiError):
        query.set_os_type([1])
    with pytest.raises(ApiError):
        query.set_os_architecture([1])
    with pytest.raises(ApiError):
        query.set_vmwaretools_version([1])
    with pytest.raises(ApiError):
        query.exclude_appliance_uuid([1])
    with pytest.raises(ApiError):
        query.exclude_cluster_name([1])
    with pytest.raises(ApiError):
        query.exclude_datacenter_name([1])
    with pytest.raises(ApiError):
        query.exclude_esx_host_name([1])
    with pytest.raises(ApiError):
        query.exclude_esx_host_uuid([1])
    with pytest.raises(ApiError):
        query.exclude_vcenter_name([1])
    with pytest.raises(ApiError):
        query.exclude_vcenter_host_url([1])
    with pytest.raises(ApiError):
        query.exclude_vcenter_uuid([1])
    with pytest.raises(ApiError):
        query.exclude_name([1])
    with pytest.raises(ApiError):
        query.exclude_host_name([1])
    with pytest.raises(ApiError):
        query.exclude_ip_address([1])
    with pytest.raises(ApiError):
        query.exclude_device_guid([1])
    with pytest.raises(ApiError):
        query.exclude_registration_id([1])
    with pytest.raises(ApiError):
        query.exclude_eligibility([1])
    with pytest.raises(ApiError):
        query.exclude_eligibility_code([1])
    with pytest.raises(ApiError):
        query.exclude_installation_status([1])
    with pytest.raises(ApiError):
        query.exclude_installation_type([1])
    with pytest.raises(ApiError):
        query.exclude_uuid([1])
    with pytest.raises(ApiError):
        query.exclude_os_description([1])
    with pytest.raises(ApiError):
        query.exclude_os_type([1])
    with pytest.raises(ApiError):
        query.exclude_os_architecture([1])
    with pytest.raises(ApiError):
        query.exclude_vmwaretools_version([1])
    with pytest.raises(ApiError):
        query.sort_by("name", "BOGUS")


def test_search_aws_async(cbcsdk_mock):
    """Tests running the async_query on AWS."""
    def post_validate(url, body, **kwargs):
        crits = body['criteria']
        assert crits['deployment_type'] == ['AWS']
        assert crits['id'] == ['7001']
        assert body['sort'] == [{"field": "name", "order": "ASC"}]

        return SEARCH_AWS_RESOURCES

    cbcsdk_mock.mock_request("POST", "/lcm/view/v2/orgs/test/compute_resources/_search",
                             post_validate)
    api = cbcsdk_mock.api
    query = api.select(AWSComputeResource).set_id(['7001']).sort_by("name", "ASC")

    assert query._count() == 1
    results = [result for result in query._run_async_query(None)]
    assert len(results) == 1
    resource = results[0]
    assert resource.id == "7001"


def test_search_aws_with_all_bells_and_whistles(cbcsdk_mock):
    """Tests running the query with all values set."""
    def post_validate(url, body, **kwargs):
        crits = body['criteria']
        assert crits['deployment_type'] == ['AWS']
        assert crits['auto_scaling_group_name'] == ['GammaGroup']
        assert crits['availability_zone'] == ['us-west-1c']
        assert crits['cloud_provider_account_id'] == ['0112249969']
        assert crits['cloud_provider_resource_id'] == ['XAW11']
        assert crits['cloud_provider_tags'] == ['Name##Demo-ASG']
        assert crits['id'] == ['7001']
        assert crits['installation_status'] == ['NOT_INSTALLED']
        assert crits['name'] == ['Demo-ASG']
        assert crits['platform'] == ['Unix/Linux']
        assert crits['platform_details'] == ['Linux/UNIX']
        assert crits['region'] == ['us-west-1']
        assert crits['subnet_id'] == ['3303']
        assert crits['virtual_private_cloud_id'] == ['90210']

        excls = body['exclusions']
        assert excls['auto_scaling_group_name'] == ['LambdaGroup']
        assert excls['availability_zone'] == ['eu-east-1x']
        assert excls['cloud_provider_account_id'] == ['9952230124']
        assert excls['cloud_provider_resource_id'] == ['XBS54']
        assert excls['cloud_provider_tags'] == ['Name##Blort-ASG']
        assert excls['id'] == ['4244']
        assert excls['installation_status'] == ['SUCCESS']
        assert excls['name'] == ['Blort-ASG']
        assert excls['platform'] == ['Solaris']
        assert excls['platform_details'] == ['Slowlaris']
        assert excls['region'] == ['eu-east-1']
        assert excls['subnet_id'] == ['5150']
        assert excls['virtual_private_cloud_id'] == ['10016']

        return SEARCH_AWS_RESOURCES

    cbcsdk_mock.mock_request("POST", "/lcm/view/v2/orgs/test/compute_resources/_search",
                             post_validate)
    api = cbcsdk_mock.api
    query = api.select(AWSComputeResource).set_auto_scaling_group_name(['GammaGroup']) \
        .set_availability_zone(['us-west-1c']).set_cloud_provider_account_id(['0112249969']) \
        .set_cloud_provider_resource_id(['XAW11']).set_cloud_provider_tags(['Name##Demo-ASG']).set_id(['7001']) \
        .set_installation_status(['NOT_INSTALLED']).set_name(['Demo-ASG']).set_platform(['Unix/Linux']) \
        .set_platform_details(['Linux/UNIX']).set_region(['us-west-1']).set_subnet_id(['3303']) \
        .set_virtual_private_cloud_id(['90210']).exclude_auto_scaling_group_name(['LambdaGroup']) \
        .exclude_availability_zone(['eu-east-1x']).exclude_cloud_provider_account_id(['9952230124']) \
        .exclude_cloud_provider_resource_id(['XBS54']).exclude_cloud_provider_tags(['Name##Blort-ASG']) \
        .exclude_id(['4244']).exclude_installation_status(['SUCCESS']).exclude_name(['Blort-ASG']) \
        .exclude_platform(['Solaris']).exclude_platform_details(['Slowlaris']).exclude_region(['eu-east-1']) \
        .exclude_subnet_id(['5150']).exclude_virtual_private_cloud_id(['10016'])

    assert query._count() == 1
    results = [result for result in query._perform_query()]
    assert len(results) == 1
    resource = results[0]
    assert resource.auto_scaling_group_name == 'GammaGroup'
    assert resource.availability_zone == 'us-west-1c'
    assert resource.cloud_provider_account_id == '0112249969'
    assert resource.cloud_provider_resource_id == 'XAW11'
    assert resource.id == '7001'
    assert resource.installation_status == 'NOT_INSTALLED'
    assert resource.name == 'Demo-ASG'
    assert resource.platform == 'Unix/Linux'
    assert resource.platform_details == 'Linux/UNIX'
    assert resource.region == 'us-west-1'
    assert resource.subnet_id == '3303'
    assert resource.virtual_private_cloud_id == '90210'


def test_search_aws_failures(cbcsdk_mock):
    """Testng all set methods for failure."""
    query = cbcsdk_mock.api.select(AWSComputeResource)
    with pytest.raises(ApiError):
        query.set_auto_scaling_group_name([1])
    with pytest.raises(ApiError):
        query.set_availability_zone([1])
    with pytest.raises(ApiError):
        query.set_cloud_provider_account_id([1])
    with pytest.raises(ApiError):
        query.set_cloud_provider_resource_id([1])
    with pytest.raises(ApiError):
        query.set_cloud_provider_tags([1])
    with pytest.raises(ApiError):
        query.set_id([1])
    with pytest.raises(ApiError):
        query.set_installation_status([1])
    with pytest.raises(ApiError):
        query.set_name([1])
    with pytest.raises(ApiError):
        query.set_platform([1])
    with pytest.raises(ApiError):
        query.set_platform_details([1])
    with pytest.raises(ApiError):
        query.set_region([1])
    with pytest.raises(ApiError):
        query.set_subnet_id([1])
    with pytest.raises(ApiError):
        query.set_virtual_private_cloud_id([1])
    with pytest.raises(ApiError):
        query.exclude_auto_scaling_group_name([1])
    with pytest.raises(ApiError):
        query.exclude_availability_zone([1])
    with pytest.raises(ApiError):
        query.exclude_cloud_provider_account_id([1])
    with pytest.raises(ApiError):
        query.exclude_cloud_provider_resource_id([1])
    with pytest.raises(ApiError):
        query.exclude_cloud_provider_tags([1])
    with pytest.raises(ApiError):
        query.exclude_id([1])
    with pytest.raises(ApiError):
        query.exclude_installation_status([1])
    with pytest.raises(ApiError):
        query.exclude_name([1])
    with pytest.raises(ApiError):
        query.exclude_platform([1])
    with pytest.raises(ApiError):
        query.exclude_platform_details([1])
    with pytest.raises(ApiError):
        query.exclude_region([1])
    with pytest.raises(ApiError):
        query.exclude_subnet_id([1])
    with pytest.raises(ApiError):
        query.exclude_virtual_private_cloud_id([1])
