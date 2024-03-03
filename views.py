import logging

from django.db import transaction
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Master_Data, Working_Sheet_Log
from .serializers import MasterDataSerializer, ModifyReasonSerializer, WorkingSheetLogSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


logger = logging.getLogger(__name__)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_qr(request, visible_material_no, username, depot_id, region_id):
    # addQr method
    if request.method == 'PUT':
        # Check if the requested username matches the logged-in user
        if request.user.username != username:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.user_level_id > 4:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # this code snippet is used to validate,
        # visual material number, depot_id and region_id
        # if they are not there, a 404 error will be passed
        try:
            log = Master_Data.objects.get(visible_material_no=visible_material_no, depot_id=depot_id,
                                          region_id=region_id)
        except Master_Data.DoesNotExist:
            error_message = f'A log with Visible Material Number [ {visible_material_no} ] at Region [ {region_id} ] Depot [ {depot_id} ] does not exist.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = MasterDataSerializer(log, data=request.data, partial=True)
            # Check if the log is active
            if log.active == 1:
                # Check if the qr is null or qr is an empty string
                if log.qr_id is None or log.qr_id == "":
                    # Check if the new QR ID is similar to any other existing QR IDs
                    if Master_Data.objects.filter(qr_id=request.data['qr_id']).exclude(pk=log.material_no).exists():
                        error_message = f"A log with the same QR ID already exists"
                        return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
                    elif serializer.is_valid():
                        # Save the updated log
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    error_message = 'Provided details are not acceptable. Try again!'
                    return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
                else:
                    error_message = f"QR is already assigned"
                    return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
            else:
                error_message = f"The log is not active"
                return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            error_message = str(e)
            logger.exception('Error in addQr method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def modify_qr(request, visible_material_no, username, depot_id, region_id):
    # modifyQr method
    if request.method == 'PUT':
        # Check if the requested username matches the logged-in user
        if request.user.username != username:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.user_level_id > 3:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        # this code snippet is used to validate,
        # visual material number, depot_id and region_id
        # if they are not there, a 404 error will be passed
        try:
            log = Master_Data.objects.get(visible_material_no=visible_material_no, depot_id=depot_id,
                                          region_id=region_id)
        except Master_Data.DoesNotExist:
            error_message = f'The log with Visible Material Number [ {visible_material_no} ] at Region [ {region_id} ] Depot [ {depot_id} ] does not exist.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = MasterDataSerializer(log, data=request.data, partial=True)

            # Extract the 'reason' from the request data
            reason = request.data.get('reason')

            # Check if the log is active
            if log.active == 1:
                # Make sure qr id is not null or an empty string
                if log.qr_id is not None and log.qr_id != "":
                    # Make sure a reason is provided
                    if reason is not None and reason != "":
                        # Check if the new QR ID is the same as before
                        if request.data['qr_id'] == log.qr_id:
                            error_message = f"The provided QR ID is the same as the existing one"
                            return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
                        # Check if the new QR ID is similar to any other existing QR IDs
                        elif Master_Data.objects.filter(qr_id=request.data['qr_id']).exclude(pk=log.material_no).exists():
                            error_message = f"A log with the same QR ID already exists"
                            return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
                        elif serializer.is_valid():
                            # Save the updated log
                            serializer.save()

                            # Add record to Modify_Reason table
                            modify_reason_data = {
                                'user': request.user.id,
                                'log': log.material_no,
                                'reason': reason,
                            }
                            modify_reason_serializer = ModifyReasonSerializer(data=modify_reason_data)
                            if modify_reason_serializer.is_valid():
                                modify_reason_serializer.save()

                            return Response(serializer.data, status=status.HTTP_200_OK)
                        error_message = 'Provided details are not acceptable. Try again!'
                        return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
                    else:
                        error_message = f"A reason must be provided to modify the QR ID"
                        return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
                else:
                    error_message = f"A QR ID must be there to modify"
                    return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
            else:
                error_message = f"The log is not active"
                return Response({'error': error_message}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            error_message = str(e)
            logger.exception('Error in modifyQr method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logs_from_visible_material_no(request, visible_material_nos, username, depot_id, region_id):
    # workingSheetFromVisualMaterialNumber method
    if request.method == 'GET':

        # Check if the requested username matches the logged-in user
        if request.user.username != username:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.user_level_id > 3:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Split the input QR IDs separated by commas
        visible_material_no_list = visible_material_nos.split(',')

        logs_data = []
        errors = []
        working_sheet_records = []

        # this code snippet is used to validate,
        # visual material number, depot_id and region_id
        # if they are not there, a 404 error will be passed
        try:
            with transaction.atomic():
                # Generate lot_id dynamically with row-level locking
                latest_working_sheet = Working_Sheet_Log.objects.select_for_update().order_by('-lot_id').first()

                if latest_working_sheet and '-' in latest_working_sheet.lot_id:
                    lot_number = int(latest_working_sheet.lot_id.split('-')[1]) + 1
                else:
                    lot_number = 1

                new_lot_id = f"lot-{lot_number}"

            for visible_material_no in visible_material_no_list:
                try:
                    log = Master_Data.objects.get(visible_material_no=visible_material_no, depot_id=depot_id,
                                                  region_id=region_id)
                    if log.active == 1:
                        serializer = MasterDataSerializer(log)
                        logs_data.append(serializer.data)

                        # Adding a record to working_sheet_log table
                        working_sheet_record = {
                            'user': request.user.id,
                            'log': log.material_no,
                            'lot_id': new_lot_id,
                        }
                       #working_sheet_records.append(working_sheet_record)
                    else: 
                        error_message = f"[{log.visible_material_no}] - The log is not active "
                        errors.append(error_message)

                except Master_Data.DoesNotExist:
                    error_message = f'A log with Visible Material Number [ {visible_material_no} ] at Region [ {region_id} ] Depot [ {depot_id} ] does not exist.'
                    errors.append(error_message)

            if errors:
                # If there are errors, return them without logs and without saving to the working_sheet_log table
                return Response({'errors': errors}, status=status.HTTP_404_NOT_FOUND)

            for record in working_sheet_records:
                working_sheet_serializer = WorkingSheetLogSerializer(data=record)
                if working_sheet_serializer.is_valid():
                    working_sheet_serializer.save()

            return Response(logs_data, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = str(e)
            logger.exception('Error in workingSheet (Visible Material Number) method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logs_from_qr_id(request, username, qr_ids):
    # workingSheetFromQRID method
    if request.method == 'GET':
        # Check if the requested username matches the logged-in user
        if request.user.username != username:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.user_level_id > 3:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Split the input QR IDs separated by commas
        qr_id_list = qr_ids.split(',')

        logs_data = []
        errors = []
        working_sheet_records = []

        try:
            with transaction.atomic():
                # Generate lot_id dynamically with row-level locking
                latest_working_sheet = Working_Sheet_Log.objects.select_for_update().order_by('-lot_id').first()

                if latest_working_sheet and '-' in latest_working_sheet.lot_id:
                    lot_number = int(latest_working_sheet.lot_id.split('-')[1]) + 1
                else:
                    lot_number = 1

                new_lot_id = f"lot-{lot_number}"

            for qr_id in qr_id_list:
                # Validate each QR ID
                try:
                    
                    log = Master_Data.objects.get(qr_id=qr_id)
                    serializer = MasterDataSerializer(log)
                    if log.active ==1:
                        logs_data.append(serializer.data)

                        # Adding a record to working_sheet_log table
                        
                    else: 
                        error_message = f"[{log.visible_material_no}] - The log is not active "
                        errors.append(error_message)
                except Master_Data.DoesNotExist:
                    error_message = f'The log with QR ID [ {qr_id} ] does not exist.'
                    errors.append(error_message)
        
            if errors:
                # If there are errors, return them without logs and without saving to the working_sheet_log table
                return Response({'errors': errors}, status=status.HTTP_404_NOT_FOUND)

            for record in working_sheet_records:
                working_sheet_serializer = WorkingSheetLogSerializer(data=record)
                if working_sheet_serializer.is_valid():
                    working_sheet_serializer.save()

            return Response(logs_data, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = str(e)
            logger.exception('Error in workingSheet (QR ID) method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_log_by_qr(request, username, qr_ids):
    # workingSheetFromQRID method
    if request.method == 'GET':
        # Check if the requested username matches the logged-in user
        if request.user.username != username:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.user_level_id > 3:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Split the input QR IDs separated by commas
        qr_id_list = qr_ids.split(',')

        logs_data = []
        errors = []
        working_sheet_records = []

        try:
            with transaction.atomic():
                # Generate lot_id dynamically with row-level locking
                latest_working_sheet = Working_Sheet_Log.objects.select_for_update().order_by('-lot_id').first()

                if latest_working_sheet and '-' in latest_working_sheet.lot_id:
                    lot_number = int(latest_working_sheet.lot_id.split('-')[1]) + 1
                else:
                    lot_number = 1

                new_lot_id = f"lot-{lot_number}"

            for qr_id in qr_id_list:
                # Validate each QR ID
                try:
                    log = Master_Data.objects.get(qr_id=qr_id)
                    serializer = MasterDataSerializer(log)
                    logs_data.append(serializer.data)

                    # Adding a record to working_sheet_log table
                    working_sheet_record = {
                        'user': request.user.id,
                        'log': log.material_no,
                        'lot_id': new_lot_id
                    }
                    #working_sheet_records.append(working_sheet_record)

                except Master_Data.DoesNotExist :
                    error_message = f'The log with QR ID [ {qr_id} ] does not exist.'
                    errors.append(error_message)

            if errors:
                # If there are errors, return them without logs and without saving to the working_sheet_log table
                return Response({'errors': errors}, status=status.HTTP_404_NOT_FOUND)

            for record in working_sheet_records:
                working_sheet_serializer = WorkingSheetLogSerializer(data=record)
                if working_sheet_serializer.is_valid():
                    working_sheet_serializer.save()

            return Response(logs_data, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = str(e)
            logger.exception('Error in workingSheet (QR ID) method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def save_working_sheet_qr(request, username,qr_ids):
    if request.method == 'GET':

        # Check if the requested username matches the logged-in user
        if request.user.username != username:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.user_level_id > 3:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # if str(request.user.depot.depot_id) != depot_id:
        #     return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Split the input QR IDs separated by commas
        qr_id_list = qr_ids.split(',')

        errors = []
        log_list_string = ""

        # this code snippet is used to validate,
        # visual material number, depot_id and region_id
        # if they are not there, a 404 error will be passed
        try:
            with transaction.atomic():
                # Generate lot_id dynamically with row-level locking
                latest_working_sheet = Working_Sheet_Log.objects.select_for_update().order_by('-lot_id').first()

                if latest_working_sheet and '-' in latest_working_sheet.lot_id:
                    lot_number = int(latest_working_sheet.lot_id.split('-')[1]) + 1
                else:
                    lot_number = 1

                new_lot_id = f"lot-{lot_number}"
            material_numbers = []
            for qr_id in qr_id_list:
                try:
                    log = Master_Data.objects.get(qr_id=qr_id, depot_id=str(request.user.depot.depot_id))
                    material_numbers.append(str(log.material_no))
                    

                except Master_Data.DoesNotExist:
                    error_message = f'A log with QR ID [ {qr_id} ] at Depot [ {str(request.user.depot.depot_id)} ] does not exist.'
                    errors.append(error_message)
            log_list_string = ', '.join(material_numbers)
            working_sheet_record = {
                        'user': request.user.id,
                        'log_list': log_list_string,
                        'lot_id': new_lot_id,
                    }
            if errors:
                # If there are errors, return them without logs and without saving to the working_sheet_log table
                return Response({'errors': errors}, status=status.HTTP_404_NOT_FOUND)

            
            working_sheet_serializer = WorkingSheetLogSerializer(data=working_sheet_record)
            if working_sheet_serializer.is_valid():
                working_sheet_serializer.save()

            return Response({'response' : "The Lot Has Created"}, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = str(e)
            logger.exception('Error in workingSheet (QR ID) method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def save_working_sheet_vmn(request, username,depot_id,visible_material_nos):
    if request.method == 'GET':

        # Check if the requested username matches the logged-in user
        if request.user.username != username:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.user_level_id > 3:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Split the input QR IDs separated by commas
        visible_material_no_list = visible_material_nos.split(',')

        errors = []
        log_list_string = ""

        # this code snippet is used to validate,
        # visual material number, depot_id and region_id
        # if they are not there, a 404 error will be passed
        try:
            with transaction.atomic():
                # Generate lot_id dynamically with row-level locking
                latest_working_sheet = Working_Sheet_Log.objects.select_for_update().order_by('-lot_id').first()

                if latest_working_sheet and '-' in latest_working_sheet.lot_id:
                    lot_number = int(latest_working_sheet.lot_id.split('-')[1]) + 1
                else:
                    lot_number = 1

                new_lot_id = f"lot-{lot_number}"
            material_numbers = []
            for visible_material_no in visible_material_no_list:
                try:
                    log = Master_Data.objects.get(visible_material_no=visible_material_no, depot_id=depot_id)
                    if log.active == 1:
                        material_numbers.append(str(log.material_no))
                    else:
                        error_message = f"[{log.visible_material_no}] - The log is not active "
                        errors.append(error_message)

                except Master_Data.DoesNotExist:
                    error_message = f'A log with Visible Material Number [ {visible_material_no} ] at Depot [ {depot_id} ] does not exist.'
                    errors.append(error_message)
            log_list_string = ', '.join(material_numbers)
            working_sheet_record = {
                        'user': request.user.id,
                        'log_list': log_list_string,
                        'lot_id': new_lot_id,
                    }
            if errors:
                # If there are errors, return them without logs and without saving to the working_sheet_log table
                return Response({'errors': errors}, status=status.HTTP_404_NOT_FOUND)

            
            working_sheet_serializer = WorkingSheetLogSerializer(data=working_sheet_record)
            if working_sheet_serializer.is_valid():
                working_sheet_serializer.save()
            return Response({'response' : "The Lot Has Created"}, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = str(e)
            logger.exception('Error in workingSheet (Visible Material Number) method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



