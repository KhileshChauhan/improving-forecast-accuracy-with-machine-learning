# #####################################################################################################################
#  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                            #
#                                                                                                                     #
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance     #
#  with the License. A copy of the License is located at                                                              #
#                                                                                                                     #
#  http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                     #
#  or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES  #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions     #
#  and limitations under the License.                                                                                 #
# #####################################################################################################################

from shared.Dataset.dataset_file import DatasetFile
from shared.config import Config
from shared.helpers import step_function_step
from shared.status import Status


@step_function_step
def createpredictor(event, context) -> (Status, str):
    """
    Create/ monitor Amazon Forecast predictor creation
    :param event: lambda event
    :param context: lambda context
    :return: predictor status and dataset ARN
    """
    config = Config.from_sfn(event)
    dataset_file = DatasetFile(event.get("dataset_file"), event.get("bucket"))
    dataset_group_name = event.get("dataset_group_name")

    predictor = config.predictor(dataset_file, dataset_group_name)
    if predictor.status == Status.DOES_NOT_EXIST:
        predictor.create()

    return predictor.status, predictor.arn
